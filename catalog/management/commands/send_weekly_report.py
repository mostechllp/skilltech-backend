import datetime
from django.core.management.base import BaseCommand
from django.utils import timezone
from django.db.models import Count
from django.core.mail import send_mail, get_connection
from django.conf import settings
from catalog.models import VisitorLog, SiteSettings


def generate_weekly_report_data():
    now = timezone.now()
    week_ago = now - datetime.timedelta(days=7)
    two_weeks_ago = now - datetime.timedelta(days=14)

    # Current 7 days
    curr_qs = VisitorLog.objects.filter(created_at__gte=week_ago, is_bot=False)
    curr_total = curr_qs.count()
    curr_unique = curr_qs.values('ip_address').distinct().count()

    # Previous 7 days
    prev_qs = VisitorLog.objects.filter(created_at__gte=two_weeks_ago, created_at__lt=week_ago, is_bot=False)
    prev_total = prev_qs.count()
    prev_unique = prev_qs.values('ip_address').distinct().count()

    # Growth calculation
    if prev_total > 0:
        growth_pct = round(((curr_total - prev_total) / prev_total) * 100, 1)
        growth_str = f"{'+' if growth_pct >= 0 else ''}{growth_pct}%"
    else:
        growth_str = "N/A (First Week)"

    # Top 10 Visited Pages
    top_pages = list(
        curr_qs.values('path')
        .annotate(views=Count('id'))
        .order_by('-views')[:10]
    )

    # Top 5 Countries
    top_countries = list(
        curr_qs.values('country')
        .annotate(views=Count('id'))
        .order_by('-views')[:5]
    )

    # Devices
    device_counts = dict(
        curr_qs.values('device_type')
        .annotate(views=Count('id'))
        .values_list('device_type', 'views')
    )
    desktop_cnt = device_counts.get('desktop', 0)
    mobile_cnt = device_counts.get('mobile', 0)
    tablet_cnt = device_counts.get('tablet', 0)

    total_devices = max(desktop_cnt + mobile_cnt + tablet_cnt, 1)
    desktop_pct = round((desktop_cnt / total_devices) * 100, 1)
    mobile_pct = round((mobile_cnt / total_devices) * 100, 1)
    tablet_pct = round((tablet_cnt / total_devices) * 100, 1)

    return {
        'start_date': week_ago.strftime('%b %d, %Y'),
        'end_date': now.strftime('%b %d, %Y'),
        'curr_total': curr_total,
        'curr_unique': curr_unique,
        'prev_total': prev_total,
        'prev_unique': prev_unique,
        'growth_str': growth_str,
        'top_pages': top_pages,
        'top_countries': top_countries,
        'desktop_cnt': desktop_cnt,
        'desktop_pct': desktop_pct,
        'mobile_cnt': mobile_cnt,
        'mobile_pct': mobile_pct,
        'tablet_cnt': tablet_cnt,
        'tablet_pct': tablet_pct,
    }


def build_email_html(data):
    top_pages_rows = "".join(
        f"""<tr>
            <td style="padding: 10px 12px; border-bottom: 1px solid #eee; font-size: 13px; color: #333;">
                <code style="background: #f4f6f8; padding: 2px 6px; border-radius: 4px; color: #062e5c;">{p['path']}</code>
            </td>
            <td style="padding: 10px 12px; border-bottom: 1px solid #eee; text-align: right; font-weight: 600; color: #333;">
                {p['views']:,}
            </td>
        </tr>"""
        for p in data['top_pages']
    ) or '<tr><td colspan="2" style="padding: 12px; text-align: center; color: #888;">No page hits recorded yet.</td></tr>'

    top_countries_rows = "".join(
        f"""<tr>
            <td style="padding: 10px 12px; border-bottom: 1px solid #eee; font-size: 13px; color: #333;">
                {c['country']}
            </td>
            <td style="padding: 10px 12px; border-bottom: 1px solid #eee; text-align: right; font-weight: 600; color: #333;">
                {c['views']:,}
            </td>
        </tr>"""
        for c in data['top_countries']
    ) or '<tr><td colspan="2" style="padding: 12px; text-align: center; color: #888;">No country data recorded yet.</td></tr>'

    return f"""<!DOCTYPE html>
<html>
<head>
<meta charset="utf-8">
<title>Skilltech Weekly Traffic Report</title>
</head>
<body style="margin: 0; padding: 20px; font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, Helvetica, Arial, sans-serif; background-color: #f7f9fa;">
<div style="max-width: 650px; margin: 0 auto; background: #ffffff; border-radius: 12px; overflow: hidden; box-shadow: 0 4px 16px rgba(0,0,0,0.06); border: 1px solid #e9ecef;">
    
    <!-- HEADER -->
    <div style="background: linear-gradient(135deg, #062e5c 0%, #0a468c 100%); padding: 30px 24px; text-align: center; color: #ffffff;">
        <h1 style="margin: 0; font-size: 24px; font-weight: 700; letter-spacing: 0.5px;">Skilltech Visitor Analytics</h1>
        <p style="margin: 6px 0 0; font-size: 14px; opacity: 0.9;">Weekly Traffic Summary ({data['start_date']} – {data['end_date']})</p>
    </div>

    <!-- MAIN METRIC CARDS -->
    <div style="padding: 24px;">
        <table style="width: 100%; border-collapse: separate; border-spacing: 12px 0; margin-bottom: 24px;">
            <tr>
                <td style="width: 50%; background: #f8fafc; border: 1px solid #e2e8f0; border-radius: 8px; padding: 18px; text-align: center;">
                    <div style="font-size: 12px; text-transform: uppercase; color: #64748b; font-weight: 600; letter-spacing: 0.5px;">Total Visits</div>
                    <div style="font-size: 28px; font-weight: 700; color: #062e5c; margin-top: 6px;">{data['curr_total']:,}</div>
                    <div style="font-size: 12px; color: #10b981; margin-top: 4px; font-weight: 500;">Growth: {data['growth_str']}</div>
                </td>
                <td style="width: 50%; background: #f8fafc; border: 1px solid #e2e8f0; border-radius: 8px; padding: 18px; text-align: center;">
                    <div style="font-size: 12px; text-transform: uppercase; color: #64748b; font-weight: 600; letter-spacing: 0.5px;">Unique Visitors</div>
                    <div style="font-size: 28px; font-weight: 700; color: #cc0070; margin-top: 6px;">{data['curr_unique']:,}</div>
                    <div style="font-size: 12px; color: #64748b; margin-top: 4px;">Distinct IPs</div>
                </td>
            </tr>
        </table>

        <!-- DEVICE BREAKDOWN -->
        <div style="background: #ffffff; border: 1px solid #e2e8f0; border-radius: 8px; padding: 16px; margin-bottom: 24px;">
            <div style="font-size: 14px; font-weight: 600; color: #062e5c; margin-bottom: 12px;">Device Breakdown</div>
            <table style="width: 100%; text-align: center;">
                <tr>
                    <td style="padding: 6px;">
                        <span style="font-size: 13px; color: #64748b;">💻 Desktop:</span> 
                        <strong style="color: #333;">{data['desktop_cnt']:,} ({data['desktop_pct']}%)</strong>
                    </td>
                    <td style="padding: 6px;">
                        <span style="font-size: 13px; color: #64748b;">📱 Mobile:</span> 
                        <strong style="color: #333;">{data['mobile_cnt']:,} ({data['mobile_pct']}%)</strong>
                    </td>
                    <td style="padding: 6px;">
                        <span style="font-size: 13px; color: #64748b;">📟 Tablet:</span> 
                        <strong style="color: #333;">{data['tablet_cnt']:,} ({data['tablet_pct']}%)</strong>
                    </td>
                </tr>
            </table>
        </div>

        <!-- TOP 10 PAGES -->
        <div style="margin-bottom: 24px;">
            <div style="font-size: 15px; font-weight: 600; color: #062e5c; margin-bottom: 10px;">Top Visited Pages & Products</div>
            <table style="width: 100%; border-collapse: collapse; border: 1px solid #e2e8f0; border-radius: 6px; overflow: hidden;">
                <thead>
                    <tr style="background: #f1f5f9; text-align: left;">
                        <th style="padding: 10px 12px; font-size: 12px; color: #475569; text-transform: uppercase;">Page Path</th>
                        <th style="padding: 10px 12px; font-size: 12px; color: #475569; text-align: right; text-transform: uppercase;">Views</th>
                    </tr>
                </thead>
                <tbody>
                    {top_pages_rows}
                </tbody>
            </table>
        </div>

        <!-- TOP COUNTRIES -->
        <div style="margin-bottom: 20px;">
            <div style="font-size: 15px; font-weight: 600; color: #062e5c; margin-bottom: 10px;">Top Visitor Countries</div>
            <table style="width: 100%; border-collapse: collapse; border: 1px solid #e2e8f0; border-radius: 6px; overflow: hidden;">
                <thead>
                    <tr style="background: #f1f5f9; text-align: left;">
                        <th style="padding: 10px 12px; font-size: 12px; color: #475569; text-transform: uppercase;">Country</th>
                        <th style="padding: 10px 12px; font-size: 12px; color: #475569; text-align: right; text-transform: uppercase;">Visits</th>
                    </tr>
                </thead>
                <tbody>
                    {top_countries_rows}
                </tbody>
            </table>
        </div>

    </div>

    <!-- FOOTER -->
    <div style="background: #f8fafc; border-top: 1px solid #e2e8f0; padding: 18px 24px; text-align: center; font-size: 12px; color: #94a3b8;">
        This automated weekly traffic summary was generated by the Skilltech Admin System.
    </div>
</div>
</body>
</html>"""


def send_weekly_report_email(recipient_override=None):
    data = generate_weekly_report_data()
    html_content = build_email_html(data)

    site_settings = SiteSettings.objects.first()

    # Determine recipient
    if recipient_override:
        recipient = recipient_override
    elif site_settings and site_settings.admin_email:
        recipient = site_settings.admin_email.split(',')[0].strip()
    elif site_settings and site_settings.email:
        recipient = site_settings.email
    else:
        recipient = getattr(settings, 'WEEKLY_REPORT_EMAIL', 'info@skilltechonline.com')

    subject = f"Skilltech Weekly Visitor Report ({data['start_date']} – {data['end_date']})"
    text_message = (
        f"Skilltech Weekly Visitor Report ({data['start_date']} – {data['end_date']})\n\n"
        f"Total Visits: {data['curr_total']:,} (Growth: {data['growth_str']})\n"
        f"Unique Visitors: {data['curr_unique']:,}\n"
        f"Desktop: {data['desktop_pct']}% | Mobile: {data['mobile_pct']}%\n"
    )

    # Use SMTP credentials configured in SiteSettings (same as Quote/Contact forms)
    connection = None
    from_email = getattr(settings, 'DEFAULT_FROM_EMAIL', 'noreply@skilltechonline.com')

    if site_settings and site_settings.email_host and site_settings.email_host_user:
        connection = get_connection(
            host=site_settings.email_host,
            port=getattr(settings, 'EMAIL_PORT', 587),
            username=site_settings.email_host_user,
            password=site_settings.email_host_password,
            use_tls=getattr(settings, 'EMAIL_USE_TLS', True),
            timeout=10,
        )
        from_email = site_settings.email_host_user

    send_mail(
        subject=subject,
        message=text_message,
        from_email=from_email,
        recipient_list=[recipient],
        html_message=html_content,
        connection=connection,
        fail_silently=False,
    )
    return recipient


class Command(BaseCommand):
    help = 'Sends the weekly website visitor summary email to Skilltech management'

    def add_arguments(self, parser):
        parser.add_argument('--email', type=str, help='Recipient email address')
        parser.add_argument('--dry-run', action='store_true', help='Print report without sending email')
        parser.add_argument('--preview', action='store_true', help='Save report as HTML file and open in browser')

    def handle(self, *args, **options):
        self.stdout.write(self.style.NOTICE("Compiling weekly visitor analytics report..."))

        data = generate_weekly_report_data()
        html_content = build_email_html(data)

        if options.get('preview'):
            import os, webbrowser
            output_file = os.path.join(settings.BASE_DIR, 'weekly_report_preview.html')
            with open(output_file, 'w', encoding='utf-8') as f:
                f.write(html_content)
            self.stdout.write(self.style.SUCCESS(f"Saved report preview to: {output_file}"))
            webbrowser.open(f"file://{output_file}")
            return

        if options.get('dry_run'):
            self.stdout.write(self.style.SUCCESS(f"[DRY-RUN] Report generated:"))
            self.stdout.write(f"Total Visits: {data['curr_total']}, Unique: {data['curr_unique']}")
            return

        try:
            recipient = send_weekly_report_email(options.get('email'))
            self.stdout.write(self.style.SUCCESS(f"Successfully sent weekly report to {recipient}"))
        except Exception as e:
            self.stdout.write(self.style.ERROR(f"Failed to send email: {e}"))
