from rest_framework import viewsets, status, mixins
import logging

logger = logging.getLogger(__name__)

from .models import Category, ProductFeature, SubCategory, Product, HomepageBanner, Offer, ProductEnquiry, ContactEnquiry, ServiceBooking
from .models import ServiceFAQ, CareerApplication, GlobalLocation, HomeStatistic, ServiceStatistic,MainCategory, Client, Catalogue, Certificate, Gallery, PageBanner, BlogPost, Project, SEOPage, SiteSettings, Service
from .models import NewsCategory,NewsPost
from .serializers import CategorySerializer, SubCategorySerializer, ProductDetailSerializer,ProductListSerializer, HomepageBannerSerializer
from .serializers import OfferSerializer, ProductEnquirySerializer, ContactEnquirySerializer, ServiceBookingSerializer, ClientSerializer, CatalogueSerializer
from .serializers import  CertificateSerializer, GallerySerializer, PageBannerSerializer, BlogPostSerializer, ProjectSerializer, SEOPageSerializer, SiteSettingsSerializer
from .serializers import  ServiceSerializer, ServiceFAQSerializer, CareerApplicationSerializer, GlobalLocationSerializer, StatisticSerializer, ServiceStatisticSerializer,MainCategorySerializer
from .serializers import NewsPostSerializer
from rest_framework.decorators import action
from rest_framework.response import Response
from django.db.models import Q, Prefetch
from django.core.mail import send_mail, get_connection
from django.conf import settings
from django.template.loader import render_to_string
from django.utils.html import strip_tags
from rest_framework.pagination import PageNumberPagination
import random, string, json
from io import BytesIO
from django.http import HttpResponse, JsonResponse
from PIL import Image, ImageDraw, ImageFont
from django.views.decorators.csrf import csrf_exempt
import threading
from rest_framework.views import APIView
from django.shortcuts import get_object_or_404
from django.http import FileResponse
from django.db.models import Count,Q,Prefetch
from django.db import connection,reset_queries

class StandardResultsSetPagination(PageNumberPagination):
    page_size = 32
    page_size_query_param = 'page_size'
    max_page_size = 100

class NewsPagination(PageNumberPagination):
    page_size = 30
    page_size_query_param = "page_size"
    max_page_size = 50
class MainCategoryViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = MainCategory.objects.none()   # ✅ just to satisfy router
    serializer_class = MainCategorySerializer
    lookup_field = "slug"

    def get_queryset(self):
        # Subcategories with product counts
        subcategories_qs = (
            SubCategory.objects.filter(active=True)
            .annotate(products_count=Count("products", filter=Q(products__active=True)))
            .order_by("order", "name")
        )

        # Categories (filter flags belong here)
        categories_qs = (
            Category.objects.filter(active=True)
            .prefetch_related(
                Prefetch("subcategories", queryset=subcategories_qs, to_attr="active_subcategories")
            )
            .order_by("order", "name")
        )

        # Apply query params to CATEGORY queryset (not main category)
        qp = self.request.query_params

        if "show_in_home" in qp:
            categories_qs = categories_qs.filter(show_in_home=qp.get("show_in_home").lower() == "true")

        if "show_in_explore_home" in qp:
            categories_qs = categories_qs.filter(show_in_explore_home=qp.get("show_in_explore_home").lower() == "true")

        if "show_in_footer" in qp:
            categories_qs = categories_qs.filter(show_in_footer=qp.get("show_in_footer").lower() == "true")

        # Main categories + nested categories
        return (
            MainCategory.objects.filter(active=True)
            .prefetch_related(Prefetch("categories", queryset=categories_qs))
            .order_by("order", "name")
        )
    # 👇 ADD THIS
    def list(self, request, *args, **kwargs):
        reset_queries()  # clear previous queries

        response = super().list(request, *args, **kwargs)

        print("Total Queries:", len(connection.queries))

        for q in connection.queries:
            print(q["sql"])

        return response

class CategoryViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = Category.objects.filter(active=True).order_by('order')
    serializer_class = CategorySerializer
    lookup_field = 'slug'

    def get_queryset(self):
        subcategories_qs = SubCategory.objects.filter(active=True).annotate(
            products_count=Count('products', filter=Q(products__active=True))
        ).order_by('order')
        queryset = Category.objects.filter(active=True).order_by('order').prefetch_related(
            Prefetch('subcategories', queryset=subcategories_qs, to_attr='active_subcategories')
        )
        show_in_home = self.request.query_params.get('show_in_home')
        if show_in_home is not None:
            queryset = queryset.filter(show_in_home=show_in_home.lower() == 'true').order_by('homepage_order')
        
        show_in_explore_home = self.request.query_params.get('show_in_explore_home')
        if show_in_explore_home is not None:
            queryset = queryset.filter(show_in_explore_home=show_in_explore_home.lower() == 'true').order_by('homepage_order')

        show_in_footer = self.request.query_params.get('show_in_footer')
        if show_in_footer is not None:
            queryset = queryset.filter(show_in_footer=show_in_footer.lower() == 'true')
            
        return queryset

class SubCategoryViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = SubCategory.objects.filter(active=True, category__active=True).order_by('order')
    serializer_class = SubCategorySerializer
    lookup_field = 'slug'
    
    def get_queryset(self):
        queryset = SubCategory.objects.filter(active=True, category__active=True).annotate(
            products_count=Count('products',filter=Q(products__active=True))
        ).order_by('order')
        category_slug = self.request.query_params.get('category_slug')
        if category_slug:
            queryset = queryset.filter(category__slug=category_slug)
        return queryset

class ProductViewSet(viewsets.ReadOnlyModelViewSet):
    lookup_field = 'slug_path'
    ordering_fields = ['order']
    pagination_class = StandardResultsSetPagination

    def paginate_queryset(self, queryset):
        show_in_home = self.request.query_params.get('show_in_home')

        if show_in_home and show_in_home.lower() == 'true':
            return None  # 🚀 disable pagination

        return super().paginate_queryset(queryset)

    def get_serializer_class(self):
        if self.action == "retrieve":
            return ProductDetailSerializer
        return ProductListSerializer

    def get_queryset(self):
        queryset = Product.objects.filter(active=True, subcategory__active=True, subcategory__category__active=True).order_by('order')
        if self.action == "retrieve":
            queryset = queryset.select_related('subcategory','subcategory__category','seo').prefetch_related(
                'images',
                'specifications',
                'similar_products',
                Prefetch('features',queryset=ProductFeature.objects.select_related('feature')))
        else:
            # LIST VIEW: Only fetch basic category info
            queryset = queryset.select_related('subcategory', 'subcategory__category')
        
        category_slug = self.request.query_params.get('category_slug')
        if category_slug:
            queryset = queryset.filter(subcategory__category__slug=category_slug)
        subcategory_slug = self.request.query_params.get('subcategory_slug')
        if subcategory_slug:
            queryset = queryset.filter(subcategory__slug=subcategory_slug)
            
        arm = self.request.query_params.get('arm')
        if arm:
            queryset = queryset.filter(arm=arm)

        show_in_home = self.request.query_params.get('show_in_home')
        if show_in_home is not None:
             queryset = queryset.filter(show_in_home=show_in_home.lower() == 'true')
             
        search_query = self.request.query_params.get('search')
        if search_query:
            queryset = queryset.filter(
                Q(name__icontains=search_query) | 
                Q(description__icontains=search_query) |
                Q(title__icontains=search_query)
            )

        limit = self.request.query_params.get('limit')
        if limit:
            try:
                queryset = queryset[:int(limit)]
            except ValueError:
                pass
             
        return queryset
    
    @action(detail=True, methods=['post'])
    def enquire(self, request, slug=None):
        product = self.get_object()
        serializer = ProductEnquirySerializer(data=request.data)
        if serializer.is_valid():
            instance = serializer.save(product=product)
            
            # Send email to admin
            try:
                site_settings = SiteSettings.objects.first()
                if site_settings and site_settings.email_host and site_settings.admin_email:
                    connection = get_connection(
                        host=site_settings.email_host,
                        port=settings.EMAIL_PORT,
                        username=site_settings.email_host_user,
                        password=site_settings.email_host_password,
                        use_tls=settings.EMAIL_USE_TLS
                    )
                    
                    subject = f"Product Enquiry: {product.name} - from {instance.name}"
                    
                    context = {
                        'name': instance.name,
                        'email': instance.email,
                        'phone': instance.phone,
                        'message': instance.message,
                        'product_name': product.name,
                        'logo_url': settings.FRONTEND_URL + '/images/logo.png'
                    }
                    
                    html_message = render_to_string('emails/product_enquiry.html', context)
                    plain_message = strip_tags(html_message)
                    
                    from django.core.mail import EmailMultiAlternatives

                    # Split admin emails by comma and strip whitespace
                    admin_emails = [email.strip() for email in site_settings.admin_email.split(',') if email.strip()]
                    
                    msg = EmailMultiAlternatives(
                        subject,
                        plain_message,
                        site_settings.email_host_user, # From email
                        admin_emails, # To email list
                        connection=connection
                    )
                    msg.attach_alternative(html_message, "text/html")
                    msg.send(fail_silently=False)
                    
            except Exception as e:
                logger.error(f"Error sending product enquiry email: {e}")

            return Response({'status': 'Enquiry submitted successfully'}, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class HomepageBannerViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = HomepageBanner.objects.filter(active=True).order_by('order')
    serializer_class = HomepageBannerSerializer

class OfferViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = Offer.objects.filter(active=True).order_by('order')
    serializer_class = OfferSerializer

class ContactEnquiryViewSet(mixins.CreateModelMixin, viewsets.GenericViewSet):
    queryset = ContactEnquiry.objects.all()
    serializer_class = ContactEnquirySerializer

    def send_contact_emails(self,instance):
        logger.info("Attempting to send email...")
        try:
            site_settings = SiteSettings.objects.first()
            # logger.debug(f"Site Settings found: {site_settings}")
            if site_settings:
                 logger.info(f"Host: {site_settings.email_host}, User: {site_settings.email_host_user}, Admin Email: {site_settings.admin_email}")

            if site_settings and site_settings.email_host and site_settings.admin_email:
                logger.info("Configuring connection...")
                connection = get_connection(
                    host=site_settings.email_host,
                    port=settings.EMAIL_PORT,
                    username=site_settings.email_host_user,
                    password=site_settings.email_host_password,
                    use_tls=settings.EMAIL_USE_TLS
                )
                
                subject = f"New Contact Enquiry from {instance.name}"
                if instance.subject:
                    subject += f": {instance.subject}"
                
                context = {
                    'name': instance.name,
                    'company': instance.company,
                    'email': instance.email,
                    'phone': instance.phone,
                    'subject': instance.subject,
                    'message': instance.comments,
                    'address': instance.address,
                    'logo_url': settings.FRONTEND_URL + '/images/logo.png'
                }
                
                html_message = render_to_string('emails/contact_enquiry.html', context)
                plain_message = strip_tags(html_message)
                
                from django.core.mail import EmailMultiAlternatives

                # Split admin emails by comma and strip whitespace
                admin_emails = [email.strip() for email in site_settings.admin_email.split(',') if email.strip()]
                
                msg = EmailMultiAlternatives(
                    subject,
                    plain_message,
                    site_settings.email_host_user, # From email
                    admin_emails, # To email list
                    connection=connection
                )
                msg.attach_alternative(html_message, "text/html")
                logger.info("Sending email to admin...")
                msg.send(fail_silently=False)
                logger.info("Email to admin sent successfully.")

                # Send acknowledgment email to user
                user_subject = "Thank you for contacting Skill Tech"
                user_html_message = render_to_string('emails/contact_acknowledgement.html', context)
                user_plain_message = strip_tags(user_html_message)
                
                user_msg = EmailMultiAlternatives(
                    user_subject,
                    user_plain_message,
                    site_settings.email_host_user, # From email
                    [instance.email], # To user's email
                    connection=connection
                )
                user_msg.attach_alternative(user_html_message, "text/html")
                logger.info("Sending acknowledgment email to user...")
                user_msg.send(fail_silently=False)
                logger.info("Acknowledgment email sent successfully.")

            else:
                logger.warning("Missing site settings or email configuration.")

        except Exception as e:
            logger.error(f"Error sending contact enquiry email: {e}")

    def perform_create(self, serializer):
        instance = serializer.save()

        threading.Thread(
            target=self.send_contact_emails,
            args=(instance,),
            daemon=True
        ).start()
            # pass

class ServiceBookingViewSet(mixins.CreateModelMixin, viewsets.GenericViewSet):
    queryset = ServiceBooking.objects.all()
    serializer_class = ServiceBookingSerializer

    def send_booking_emails(self, instance):
        # Send email to admin
        try:
            site_settings = SiteSettings.objects.first()
            if site_settings and site_settings.email_host and site_settings.admin_email:
                connection = get_connection(
                    host=site_settings.email_host,
                    port=settings.EMAIL_PORT,
                    username=site_settings.email_host_user,
                    password=site_settings.email_host_password,
                    use_tls=settings.EMAIL_USE_TLS
                )
                
                subject = f"New Service Booking: {instance.installation_type} - {instance.name}"
                
                context = {
                    'name': instance.name,
                    'email': instance.email,
                    'phone': instance.phone,
                    'installation_type': instance.installation_type,
                    'tv_size': instance.tv_size,
                    'bracket': instance.bracket,
                    'date': instance.date,
                    'time': instance.time,
                    'logo_url': settings.FRONTEND_URL + '/images/logo.png'
                }
                
                html_message = render_to_string('emails/service_booking.html', context)
                plain_message = strip_tags(html_message)
                
                from django.core.mail import EmailMultiAlternatives

                # Split admin emails by comma and strip whitespace
                admin_emails = [email.strip() for email in site_settings.admin_email.split(',') if email.strip()]
                
                msg = EmailMultiAlternatives(
                    subject,
                    plain_message,
                    site_settings.email_host_user, # From email
                    admin_emails, # To email list
                    connection=connection
                )
                msg.attach_alternative(html_message, "text/html")
                msg.send(fail_silently=False)
                
        except Exception as e:
            logger.error(f"Error sending service booking email: {e}")

    def perform_create(self, serializer):
        instance = serializer.save()
        
        threading.Thread(
            target=self.send_booking_emails,
            args=(instance,),
            daemon=True
        ).start()

class ClientViewSet(viewsets.ReadOnlyModelViewSet):

    queryset = Client.objects.filter(active=True).order_by('order')

    serializer_class = ClientSerializer



class CatalogueViewSet(viewsets.ReadOnlyModelViewSet):

    queryset = Catalogue.objects.filter(active=True).order_by('order')

    serializer_class = CatalogueSerializer



class CertificateViewSet(viewsets.ReadOnlyModelViewSet):



    queryset = Certificate.objects.filter(active=True).order_by('order')



    serializer_class = CertificateSerializer







class GalleryViewSet(viewsets.ReadOnlyModelViewSet):







    queryset = Gallery.objects.all().order_by('-created_at')







    serializer_class = GallerySerializer







    







    def get_queryset(self):







        queryset = Gallery.objects.all().order_by('-created_at')







        category_slug = self.request.query_params.get('category_slug')







        if category_slug:







            queryset = queryset.filter(category__slug=category_slug)







        return queryset















class PageBannerViewSet(viewsets.ReadOnlyModelViewSet):















    queryset = PageBanner.objects.all()















    serializer_class = PageBannerSerializer















    lookup_field = 'page'































class BlogPostViewSet(viewsets.ReadOnlyModelViewSet):















    queryset = BlogPost.objects.filter(active=True).order_by('-created_at')















    serializer_class = BlogPostSerializer















    lookup_field = 'slug'

class ProjectViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = Project.objects.filter(active=True).order_by('order')
    serializer_class = ProjectSerializer

class SEOPageViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = SEOPage.objects.all()
    serializer_class = SEOPageSerializer
    lookup_field = 'page'

class SiteSettingsViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = SiteSettings.objects.all()
    serializer_class = SiteSettingsSerializer

    def list(self, request, *args, **kwargs):
        instance = self.get_queryset().first()
        if instance:
            serializer = self.get_serializer(instance)
            return Response(serializer.data)
        return Response({})






























class ServiceViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = Service.objects.filter(active=True)
    serializer_class = ServiceSerializer

class ServiceFAQViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = ServiceFAQ.objects.filter(active=True).order_by('order')
    serializer_class = ServiceFAQSerializer

    

class CareerApplicationViewSet(mixins.CreateModelMixin, viewsets.GenericViewSet):
    queryset = CareerApplication.objects.all()
    serializer_class = CareerApplicationSerializer

    def send_career_emails(self, instance):
        # Send email to admin
        try:
            site_settings = SiteSettings.objects.first()
            if site_settings and site_settings.email_host and site_settings.admin_email:
                connection = get_connection(
                    host=site_settings.email_host,
                    port=settings.EMAIL_PORT,
                    username=site_settings.email_host_user,
                    password=site_settings.email_host_password,
                    use_tls=settings.EMAIL_USE_TLS
                )
                
                subject = f"New Career Application: {instance.position} - {instance.name}"
                
                # Construct absolute URL for CV
                if instance.cv:
                    cv_url = settings.MEDIA_BASE_URL + instance.cv.url if hasattr(settings, 'MEDIA_BASE_URL') else instance.cv.url
                else:
                    cv_url = '#'

                context = {
                    'name': instance.name,
                    'email': instance.email,
                    'phone': instance.phone,
                    'position': instance.position,
                    'cover_letter': instance.cover_letter,
                    'cv_url': cv_url,
                    'logo_url': settings.FRONTEND_URL + '/images/logo.png'
                }
                
                html_message = render_to_string('emails/career_application.html', context)
                plain_message = strip_tags(html_message)
                
                from django.core.mail import EmailMultiAlternatives

                # Split admin emails by comma and strip whitespace
                admin_emails = [email.strip() for email in site_settings.admin_email.split(',') if email.strip()]
                
                msg = EmailMultiAlternatives(
                    subject,
                    plain_message,
                    site_settings.email_host_user, # From email
                    admin_emails, # To email list
                    connection=connection
                )
                msg.attach_alternative(html_message, "text/html")
                
                # Optionally attach the CV file directly to the email
                # if instance.cv:
                #     msg.attach_file(instance.cv.path)

                msg.send(fail_silently=False)
                
        except Exception as e:
            logger.error(f"Error sending career application email: {e}")

    def perform_create(self, serializer):
        instance = serializer.save()
        
        threading.Thread(
            target=self.send_career_emails,
            args=(instance,),
            daemon=True
        ).start()



class GlobalLocationViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = GlobalLocation.objects.filter(active=True).order_by('order')
    serializer_class = GlobalLocationSerializer

class StatisticViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = HomeStatistic.objects.filter(active=True).order_by('order')
    serializer_class = StatisticSerializer

class ServiceStatisticViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = ServiceStatistic.objects.filter(active=True).order_by('order')
    serializer_class = ServiceStatisticSerializer

class SitemapDataViewSet(viewsets.ViewSet):
    def list(self, request):
        products = Product.objects.filter(active=True, subcategory__active=True, subcategory__category__active=True).select_related('subcategory__category').values(
            'slug', 'updated_at', 'subcategory__slug', 'subcategory__category__slug','slug_path'
        )
        categories = Category.objects.filter(active=True).values('slug')
        subcategories = SubCategory.objects.filter(active=True, category__active=True).select_related('category').values('slug', 'category__slug')
        blogs = BlogPost.objects.filter(active=True).values('slug', 'created_at')

        return Response({
            'products': list(products),
            'categories': list(categories),
            'subcategories': list(subcategories),
            'blogs': list(blogs),
        })

def generate_captcha(request):
    text = ''.join(random.choices(string.ascii_uppercase + string.digits, k=5))
    request.session['captcha_text'] = text
    request.session.modified = True
    request.session.save() # Force save
    
    logger.debug(f"Generated Captcha: '{text}', Session ID: {request.session.session_key}")

    img = Image.new("RGB", (200, 70), "white")
    draw = ImageDraw.Draw(img)

    try:
        # Try to load a custom font from static files
        import os
        font_path = os.path.join(settings.BASE_DIR, 'static', 'fonts', 'captcha.ttf')
        
        if os.path.exists(font_path):
            font = ImageFont.truetype(font_path, 40)
        else:
            # Fallback to system fonts if custom font is missing
            try:
                # Common linux paths
                font = ImageFont.truetype("/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf", 40)
            except:
                font = ImageFont.truetype("arial.ttf", 40)
    except:
        font = ImageFont.load_default()

    # Draw text with some offset
    draw.text((40, 15), text, font=font, fill="black")
    
    # Add some noise lines
    for _ in range(5):
        x1 = random.randint(0, 200)
        y1 = random.randint(0, 70)
        x2 = random.randint(0, 200)
        y2 = random.randint(0, 70)
        draw.line([(x1, y1), (x2, y2)], fill="black", width=1)

    buffer = BytesIO()
    img.save(buffer, "PNG")
    buffer.seek(0)

    return HttpResponse(buffer, content_type="image/png")

@csrf_exempt
def validate_captcha(request):
    try:
        # Check if captcha is enabled globally
        settings_obj = SiteSettings.objects.first()
        if settings_obj and not settings_obj.enable_captcha:
             return JsonResponse({"status": "ok"})
    except:
        pass

    if request.method != "POST":
        return JsonResponse({"status": "invalid"}, status=400)

    try:
        data = json.loads(request.body)
        user_input = data.get("captcha")
        # Ensure session is saved and accessible. 
        # Note: Frontend must send credentials (cookies) for this to work.
        real = request.session.get("captcha_text", "")
        
        print(f"DEBUG: User Input: '{user_input}', Real Captcha: '{real}', Session ID: {request.session.session_key}")

        if user_input and real and user_input.upper() == real:
            return JsonResponse({"status": "ok"})
        else:
            print("DEBUG: Validation Failed")
            pass
    except Exception as e:
        print(f"DEBUG: Exception in validate_captcha: {e}")
        pass

    return JsonResponse({"status": "fail"})

class CatalogueThumbnailDownloadView(APIView):
    def get(self,request,pk):
        catalogue=get_object_or_404(Catalogue,pk=pk)
        if not catalogue.file:
            return Response({"message":"File not found."},status=status.HTTP_404_NOT_FOUND)
        response=FileResponse(
            catalogue.file.open(),
            as_attachment=True,
            filename=catalogue.file.name.split('/')[-1],
        )
        return response

class NewsPostViewset(viewsets.ReadOnlyModelViewSet):
    queryset=NewsPost.objects.filter(status="published")
    serializer_class=NewsPostSerializer
    pagination_class = NewsPagination