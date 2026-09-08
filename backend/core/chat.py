"""Camp Security chat assistant — FAQ matching with optional LLM upgrade."""

from __future__ import annotations

import json
import os
import re
import urllib.error
import urllib.request

from django.conf import settings

from .models import Service


def _contact_reply() -> str:
    return (
        'You can reach Camp Security at:\n'
        '• Office: (555) 123-SECURE\n'
        '• Emergency: (555) 911-SECURITY\n'
        f'• Email: {settings.CONTACT_EMAIL}\n'
        f'• Sales: {settings.SALES_EMAIL}\n'
        'Or use the Contact form on this website — we respond promptly.'
    )


def _services_blurb() -> str:
    titles = list(Service.objects.order_by('order', 'title').values_list('title', flat=True)[:8])
    if not titles:
        return ''
    return ' Current services on file: ' + ', '.join(titles) + '.'


def _score(message: str, keywords: list[str]) -> int:
    score = 0
    for kw in keywords:
        if kw in message:
            score += 2 if ' ' in kw else 1
    return score


# (keywords, reply_key or static reply string)
# reply_key: 'contact' | 'services' | 'static'
FAQ_INTENTS: list[tuple[list[str], str]] = [
    (
        ['service', 'services', 'offer', 'provide', 'what do you', 'do you do'],
        'services',
    ),
    (
        ['guard', 'guarding', 'officer', 'patrol', 'access control', 'event security', 'event'],
        'We cover guarding, mobile patrols, access control, and event security for businesses, '
        'estates, and venues. Share your site type and hours on the Contact page for a tailored quote.',
    ),
    (
        ['psira', 'registered', 'certified', 'licence', 'license', 'compliance'],
        'Our team is trained with first-aid readiness and ongoing compliance focus. '
        'For formal verification on a contract, contact the office and we will share the documents you need.',
    ),
    (
        ['price', 'pricing', 'cost', 'quote', 'how much', 'rate', 'fees'],
        'Pricing depends on site size, risk level, and coverage hours. We do not publish a flat rate online. '
        'Share your requirements on the Contact page and our team will send a quote.',
    ),
    (
        ['contact', 'phone', 'email', 'address', 'reach', 'call', 'whatsapp'],
        'contact',
    ),
    (
        ['career', 'job', 'hiring', 'vacancy', 'work for', 'join'],
        'Open roles are listed on the Careers page. Benefits typically include competitive pay, training, '
        'certification support, and career progression. Apply via Careers or email our careers inbox.',
    ),
    (
        ['hour', 'hours', '24/7', '247', 'emergency', 'night', 'weekend'],
        'We support 24/7 coverage for contracted sites. For emergencies on an active contract, use the '
        'emergency line on Contact. For new enquiries, leave a message anytime via the form.',
    ),
    (
        ['client', 'industry', 'who do you', 'retail', 'estate', 'warehouse'],
        'We support clients across industries such as retail, estates, commercial buildings, and events. '
        'See the Clients page, then Contact us for your sector.',
    ),
    (
        ['hello', 'hi', 'hey', 'good morning', 'good afternoon'],
        'Hi — I am the Camp Security assistant. Ask about services, quotes, careers, or how to contact us.',
    ),
    (
        ['thank', 'thanks'],
        'You are welcome. If you need a quote, the Contact page is the fastest next step.',
    ),
]


def faq_reply(message: str) -> tuple[str, str]:
    text = re.sub(r'\s+', ' ', message.lower().strip())

    best_score = 0
    best_payload: str | None = None

    for keywords, payload in FAQ_INTENTS:
        score = _score(text, keywords)
        if score > best_score:
            best_score = score
            best_payload = payload

    if best_score == 0 or best_payload is None:
        return (
            'I can help with services, quotes, careers, hours, and contact details. '
            'Try asking “What services do you offer?” or “How do I get a quote?” '
            'For a human reply, use the Contact page.',
            'faq',
        )

    if best_payload == 'contact':
        return _contact_reply(), 'faq'

    if best_payload == 'services':
        reply = (
            'Camp Security provides professional protection for people, property, and events - '
            'including on-site guarding, patrols, access control, and event security.'
            + _services_blurb()
            + ' Browse Services on the site, or ask for a quote via Contact.'
        )
        return reply, 'faq'

    return best_payload, 'faq'


def _llm_enabled() -> bool:
    return bool(os.environ.get('GROQ_API_KEY') or os.environ.get('OPENAI_API_KEY'))


def _camp_context() -> str:
    services = ', '.join(
        Service.objects.order_by('order', 'title').values_list('title', flat=True)[:12]
    ) or 'guarding, patrols, access control, event security'
    return (
        'You are a helpful assistant for Camp Security, a professional security company. '
        'Answer briefly (2–4 sentences). Be professional. Do not invent certifications or prices. '
        'If unsure, direct visitors to the Contact page. '
        f'Services include: {services}. '
        f'Contact email: {settings.CONTACT_EMAIL}. Sales: {settings.SALES_EMAIL}.'
    )


def llm_reply(message: str) -> str | None:
    groq_key = os.environ.get('GROQ_API_KEY')
    openai_key = os.environ.get('OPENAI_API_KEY')

    if groq_key:
        url = 'https://api.groq.com/openai/v1/chat/completions'
        key = groq_key
        model = os.environ.get('GROQ_MODEL', 'llama-3.1-8b-instant')
    elif openai_key:
        url = 'https://api.openai.com/v1/chat/completions'
        key = openai_key
        model = os.environ.get('OPENAI_MODEL', 'gpt-4o-mini')
    else:
        return None

    payload = {
        'model': model,
        'temperature': 0.3,
        'messages': [
            {'role': 'system', 'content': _camp_context()},
            {'role': 'user', 'content': message[:1000]},
        ],
    }
    req = urllib.request.Request(
        url,
        data=json.dumps(payload).encode('utf-8'),
        headers={
            'Content-Type': 'application/json',
            'Authorization': f'Bearer {key}',
        },
        method='POST',
    )
    try:
        with urllib.request.urlopen(req, timeout=20) as resp:
            data = json.loads(resp.read().decode('utf-8'))
        content = data['choices'][0]['message']['content'].strip()
        return content or None
    except (
        urllib.error.URLError,
        urllib.error.HTTPError,
        KeyError,
        IndexError,
        TimeoutError,
        json.JSONDecodeError,
        ValueError,
    ):
        return None


def get_reply(message: str, prefer_llm: bool = True) -> dict:
    cleaned = (message or '').strip()
    if len(cleaned) < 2:
        return {'reply': 'Please type a short question about Camp Security.', 'mode': 'faq'}
    if len(cleaned) > 1000:
        cleaned = cleaned[:1000]

    if prefer_llm and _llm_enabled():
        llm_text = llm_reply(cleaned)
        if llm_text:
            return {'reply': llm_text, 'mode': 'llm'}

    reply, mode = faq_reply(cleaned)
    return {'reply': reply, 'mode': mode}
