"""Start the Next.js site when `python manage.py runserver` is used."""

from __future__ import annotations

import atexit
import os
import socket
import subprocess
import sys
import time
from pathlib import Path

FRONTEND_URL = os.environ.get('FRONTEND_URL', 'http://localhost:3000')
FRONTEND_PORT = int(os.environ.get('FRONTEND_PORT', '3000'))
FRONTEND_DIR = Path(__file__).resolve().parent.parent.parent / 'frontend'

DEFAULT_API_PORT = 8000
FALLBACK_API_PORTS = (9000, 7000, 5000, 4000)

_process: subprocess.Popen | None = None


def can_bind_port(port: int, host: str = '127.0.0.1') -> bool:
    """Return True if this process can listen on host:port."""
    try:
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as sock:
            sock.bind((host, port))
        return True
    except OSError:
        return False


def _runserver_addrport(argv: list[str]) -> str | None:
    seen = False
    for arg in argv:
        if arg == 'runserver':
            seen = True
            continue
        if seen and not arg.startswith('-'):
            return arg
    return None


def _port_from_addrport(addrport: str) -> int:
    if ':' in addrport:
        return int(addrport.rsplit(':', 1)[-1])
    return int(addrport)


def _sync_env_local(api_url: str) -> None:
    if 'test' in sys.argv:
        return
    path = FRONTEND_DIR / '.env.local'
    if not path.exists():
        return
    lines = path.read_text(encoding='utf-8').splitlines()
    updated = False
    for index, line in enumerate(lines):
        if line.startswith('NEXT_PUBLIC_API_URL=http://localhost:'):
            lines[index] = f'NEXT_PUBLIC_API_URL={api_url}'
            updated = True
            break
    if updated:
        path.write_text('\n'.join(lines) + '\n', encoding='utf-8')


def _set_frontend_api_url(port: int) -> None:
    api_url = f'http://localhost:{port}/api'
    os.environ['NEXT_PUBLIC_API_URL'] = api_url
    _sync_env_local(api_url)


def configure_runserver_port(argv: list[str]) -> int:
    """Make sure runserver uses a port Windows will actually allow."""
    existing = _runserver_addrport(argv)
    if existing is not None:
        port = _port_from_addrport(existing)
        _set_frontend_api_url(port)
        return port

    for port in (DEFAULT_API_PORT, *FALLBACK_API_PORTS):
        if not can_bind_port(port):
            continue
        argv.insert(argv.index('runserver') + 1, str(port))
        _set_frontend_api_url(port)
        if port != DEFAULT_API_PORT and 'test' not in sys.argv:
            print(
                f'Port {DEFAULT_API_PORT} is reserved by Windows on this machine. '
                f'API: http://127.0.0.1:{port}/'
            )
        return port

    _set_frontend_api_url(DEFAULT_API_PORT)
    return DEFAULT_API_PORT


def _port_is_open(port: int) -> bool:
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as sock:
        sock.settimeout(0.3)
        return sock.connect_ex(('127.0.0.1', port)) == 0


def _npm(*args: str) -> list[str]:
    if sys.platform == 'win32':
        return ['cmd', '/c', 'npm', *args]
    return ['npm', *args]


def _stop_frontend() -> None:
    global _process
    if _process is None or _process.poll() is not None:
        return
    if sys.platform == 'win32':
        subprocess.call(
            ['taskkill', '/F', '/T', '/PID', str(_process.pid)],
            stdout=subprocess.DEVNULL,
            stderr=subprocess.DEVNULL,
        )
    else:
        _process.terminate()
        try:
            _process.wait(timeout=5)
        except subprocess.TimeoutExpired:
            _process.kill()
    _process = None


def ensure_frontend() -> None:
    """Launch Next.js once from the runserver parent process."""
    if os.environ.get('RUN_MAIN') == 'true':
        return
    if not (FRONTEND_DIR / 'package.json').exists():
        return
    if _port_is_open(FRONTEND_PORT):
        print(f'Website: {FRONTEND_URL}')
        return

    env_example = FRONTEND_DIR / '.env.example'
    env_local = FRONTEND_DIR / '.env.local'
    if not env_local.exists() and env_example.exists():
        env_local.write_text(env_example.read_text(encoding='utf-8'), encoding='utf-8')
    api_url = os.environ.get('NEXT_PUBLIC_API_URL')
    if api_url:
        _sync_env_local(api_url)

    if not (FRONTEND_DIR / 'node_modules').exists():
        print('Installing frontend dependencies (first run only)...')
        subprocess.check_call(_npm('install'), cwd=FRONTEND_DIR)

    global _process
    _process = subprocess.Popen(_npm('run', 'dev'), cwd=FRONTEND_DIR)
    atexit.register(_stop_frontend)

    for _ in range(60):
        if _port_is_open(FRONTEND_PORT):
            print(f'Website: {FRONTEND_URL}')
            return
        if _process.poll() is not None:
            break
        time.sleep(0.5)

    print(
        'Could not start the website automatically. '
        'From the frontend folder run: npm run dev'
    )
