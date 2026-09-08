'use client';

export default function Error({
  error,
  reset,
}: {
  error: Error & { digest?: string };
  reset: () => void;
}) {
  const isConnectionError =
    error.message.includes('fetch failed') ||
    error.message.includes('ECONNREFUSED') ||
    error.message.includes('API error');

  return (
    <div className="card card-inset max-w-xl">
      <div className="eyebrow">Something went wrong</div>
      <h1 className="title">{isConnectionError ? 'API not reachable' : 'Page error'}</h1>
      {isConnectionError ? (
        <p className="muted">
          The frontend could not connect to the Django API at{' '}
          <code>{process.env.NEXT_PUBLIC_API_URL || 'http://localhost:8000/api'}</code>. From the camp folder run:
        </p>
      ) : (
        <p className="muted">{error.message}</p>
      )}
      {isConnectionError && (
        <pre className="mt-4 overflow-x-auto rounded-lg border border-soft-border bg-surface p-4 text-sm text-muted">
          {`cd camp
backend\\.venv\\Scripts\\activate
python manage.py runserver`}
        </pre>
      )}
      <p className="muted mt-4">
        Website: <strong>http://localhost:3000</strong> &nbsp;|&nbsp; API:{' '}
        <strong>{process.env.NEXT_PUBLIC_API_URL || 'http://localhost:8000/api'}/health/</strong>
      </p>
      <button type="button" onClick={reset} className="btn mt-4">
        Try again
      </button>
    </div>
  );
}
