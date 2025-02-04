

from ecommerce.extensions.basket.views import MobileVoucherAddView
from django.conf.urls import include, url
from django.urls import path
from rest_framework.urlpatterns import format_suffix_patterns
from rest_framework_extensions.routers import ExtendedSimpleRouter as SimpleRouter

from ecommerce.core.constants import COURSE_ID_PATTERN, UUID_REGEX_PATTERN
from ecommerce.extensions.api.v2.views import assignmentemail as assignment_email
from ecommerce.extensions.api.v2.views import baskets as basket_views
from ecommerce.extensions.api.v2.views import catalog as catalog_views
from ecommerce.extensions.api.v2.views import checkout as checkout_views
from ecommerce.extensions.api.v2.views import coupons as coupon_views
from ecommerce.extensions.api.v2.views import courses as course_views
from ecommerce.extensions.api.v2.views import enterprise as enterprise_views
from ecommerce.extensions.api.v2.views import orders as order_views
from ecommerce.extensions.api.v2.views import partners as partner_views
from ecommerce.extensions.api.v2.views import payments as payment_views
from ecommerce.extensions.api.v2.views import products as product_views
from ecommerce.extensions.api.v2.views import providers as provider_views
from ecommerce.extensions.api.v2.views import publication as publication_views
from ecommerce.extensions.api.v2.views import refunds as refund_views
from ecommerce.extensions.api.v2.views import retirement as retirement_views
from ecommerce.extensions.api.v2.views import stockrecords as stockrecords_views
from ecommerce.extensions.api.v2.views import user_management as user_management_views
from ecommerce.extensions.api.v2.views import vouchers as voucher_views
from ecommerce.extensions.api.v2.views.gs_views import get_ephemeral_key, get_basket_content, get_basket_content_mobile, get_course_discount_info, BasketViewSet, apply_voucher_mobile
from ecommerce.extensions.api.v2.stripe_api import views as custom_stripe_view
from ecommerce.extensions.voucher.views import CouponReportCSVView

ORDER_NUMBER_PATTERN = r'(?P<number>[-\w]+)'
BASKET_ID_PATTERN = r'(?P<basket_id>[\d]+)'

# From edx-platform's lms/envs/common.py as of 2018-10-09
USERNAME_REGEX_PARTIAL = r'[\w .@_+-]+'
USERNAME_PATTERN = r'(?P<username>{regex})'.format(regex=USERNAME_REGEX_PARTIAL)

BASKET_URLS = [
    url(r'^$', basket_views.BasketCreateView.as_view(), name='create'),
    url(
        r'^{basket_id}/$'.format(basket_id=BASKET_ID_PATTERN),
        basket_views.BasketDestroyView.as_view(),
        name='destroy'
    ),
    url(
        r'^{basket_id}/order/$'.format(basket_id=BASKET_ID_PATTERN),
        basket_views.OrderByBasketRetrieveView.as_view(),
        name='retrieve_order'
    ),
    url(r'^calculate/$', basket_views.BasketCalculateView.as_view(), name='calculate'),
    #url(r'^remove/$', basket_views.BasketDeleteItemView.as_view(), name='remove-item'),
]

PAYMENT_URLS = [
    url(r'^processors/$', payment_views.PaymentProcessorListView.as_view(), name='list_processors'),
]

REFUND_URLS = [
    url(r'^$', refund_views.RefundCreateView.as_view(), name='create'),
    url(r'^(?P<pk>[\d]+)/process/$', refund_views.RefundProcessView.as_view(), name='process'),
]

RETIREMENT_URLS = [
    url(r'^tracking_id/{}/$'.format(USERNAME_PATTERN), retirement_views.EcommerceIdView.as_view(), name='tracking_id')
]

COUPON_URLS = [
    url(r'^coupon_reports/(?P<coupon_id>[\d]+)/$', CouponReportCSVView.as_view(), name='coupon_reports'),
    url(r'^categories/$', coupon_views.CouponCategoriesListView.as_view(), name='coupons_categories'),
]

CHECKOUT_URLS = [
    url(r'^$', checkout_views.CheckoutView.as_view(), name='process')
]

CUSTOM_STRIPE_URLS = [
    url(r'^$', custom_stripe_view.CustomStripeView.as_view(), name='create_customer'),
    url(r'^getToken/$', custom_stripe_view.TokenView.as_view(), name='get_token'),
]

BASKET_BUYNOW_URL = [
    url(r'^$', basket_views.CommitedBasket.as_view(), name='basket_buy_now')
]

STRIPE_PAYMENT_URLS = [
    url(r'^$', custom_stripe_view.PaymentView.as_view(), name='stripe_payment'),
]

CHECKOUT_PAYMENT_INTENT = [
    url(r'^$', custom_stripe_view.CheckoutBasketMobileView.as_view(), name='checkout_payment_intent'),
]

CONFIRM_PAYMENT_INTENT = [
    url(r'^$', custom_stripe_view.ConfirmPaymentMobileView.as_view(), name='confirm_payment_intent'),
]

CUSTOM_BASKET_URLS = [
    url(r'^$', basket_views.BasketDeleteItemView.as_view(), name='custom_baskets'),
]

BASKET_ITEM_URLS = [
    url(r'^$', basket_views.BasketItemCountView.as_view(), name='basket_item_count'),
]

ATOMIC_PUBLICATION_URLS = [
    url(r'^$', publication_views.AtomicPublicationView.as_view(), name='create'),
    url(
        r'^{course_id}$'.format(course_id=COURSE_ID_PATTERN),
        publication_views.AtomicPublicationView.as_view(),
        name='update'
    ),
]

PROVIDER_URLS = [
    url(r'^$', provider_views.ProviderViewSet.as_view(), name='list_providers')
]

ENTERPRISE_URLS = [
    url(r'^customers$', enterprise_views.EnterpriseCustomerViewSet.as_view(), name='enterprise_customers'),
    url(
        r'^customer_catalogs$',
        enterprise_views.EnterpriseCustomerCatalogsViewSet.as_view({'get': 'get'}),
        name='enterprise_customer_catalogs'
    ),
    url(
        r'^customer_catalogs/(?P<enterprise_catalog_uuid>[^/]+)$',
        enterprise_views.EnterpriseCustomerCatalogsViewSet.as_view({'get': 'retrieve'}),
        name='enterprise_customer_catalog_details'
    ),
]

ASSIGNMENT_EMAIL_URLS = [
    url(r'^status/$', assignment_email.AssignmentEmailStatus.as_view(), name='update_status'),
    url(r'^bounce$', assignment_email.AssignmentEmailBounce.as_view(), name='receive_bounce')
]

USER_MANAGEMENT_URLS = [
    url(r'^replace_usernames/$', user_management_views.UsernameReplacementView.as_view(), name='username_replacement'),
]

urlpatterns = [
    url(r'^baskets/', include((BASKET_URLS, 'baskets'))),
    url(r'^checkout/', include((CHECKOUT_URLS, 'checkout'))),
    url(r'^coupons/', include((COUPON_URLS, 'coupons'))),
    url(r'^enterprise/', include((ENTERPRISE_URLS, 'enterprise'))),
    url(r'^payment/', include((PAYMENT_URLS, 'payment'))),
    url(r'^providers/', include((PROVIDER_URLS, 'providers'))),
    url(r'^publication/', include((ATOMIC_PUBLICATION_URLS, 'publication'))),
    url(r'^refunds/', include((REFUND_URLS, 'refunds'))),
    url(r'^retirement/', include((RETIREMENT_URLS, 'retirement'))),
    url(r'^user_management/', include((USER_MANAGEMENT_URLS, 'user_management'))),
    url(r'^assignment-email/', include((ASSIGNMENT_EMAIL_URLS, 'assignment-email'))),
    url(r'^stripe_get_ephemeral_key/$', get_ephemeral_key, name='get_ephemeral_key'),
    url(r'^stripe_api/', include((CUSTOM_STRIPE_URLS, 'stripe_api'))),
    url(r'^stripe_payment/', include((STRIPE_PAYMENT_URLS, 'stripe_payment'))),
    url(r'^checkout_payment_intent/', include((CHECKOUT_PAYMENT_INTENT, 'checkout_payment_intent'))),
    url(r'^confirm_payment_intent/', include((CONFIRM_PAYMENT_INTENT, 'confirm_payment_intent'))),
    url(r'^custom_baskets/', include((CUSTOM_BASKET_URLS, 'custom_baskets'))),
    url(r'^basket_buy_now/', include((BASKET_BUYNOW_URL, 'basket_buy_now'))),
    url(r'^basket_item_count/', include((BASKET_ITEM_URLS, 'basket_item_count'))),
    url(r'^basket_details/$', get_basket_content, name='get_basket_detail'),
    url(r'^basket_details_mobile/$', get_basket_content_mobile, name='get_basket_detail_mobile'),
    url(r'^course_discount_info/(?P<sku>[\w\-]+)/$',get_course_discount_info, name='get_course_discount_info'),
    url(r'^apply_voucher_mobile/$', apply_voucher_mobile, name='apply_voucher_mobile'),

]

router = SimpleRouter()
router.register(r'basket-details', basket_views.BasketViewSet, basename='basket')
router.register(r'^get-basket-detail', BasketViewSet, basename='basket')
router.register(r'catalogs', catalog_views.CatalogViewSet, basename='catalog') \
    .register(r'products', product_views.ProductViewSet, basename='catalog-product',
              parents_query_lookups=['stockrecords__catalogs'])
router.register(r'coupons', coupon_views.CouponViewSet, basename='coupons')
router.register(r'enterprise/coupons', enterprise_views.EnterpriseCouponViewSet, basename='enterprise-coupons')
router.register(
    r'enterprise/offer_assignment_summary',
    enterprise_views.OfferAssignmentSummaryViewSet,
    basename='enterprise-offer-assignment-summary',
)
router.register(
    r'enterprise/offer-assignment-email-template/(?P<enterprise_customer>{})'.format(UUID_REGEX_PATTERN),
    enterprise_views.OfferAssignmentEmailTemplatesViewSet,
    basename='enterprise-offer-assignment-email-template',
)

router.register(r'courses', course_views.CourseViewSet, basename='course') \
    .register(r'products', product_views.ProductViewSet,
              basename='course-product', parents_query_lookups=['course_id'])
router.register(r'orders', order_views.OrderViewSet, basename='order')
router.register(
    r'manual_course_enrollment_order',
    order_views.ManualCourseEnrollmentOrderViewSet,
    basename='manual-course-enrollment-order'
)
router.register(r'partners', partner_views.PartnerViewSet) \
    .register(r'catalogs', catalog_views.CatalogViewSet,
              basename='partner-catalogs', parents_query_lookups=['partner_id'])
router.register(r'partners', partner_views.PartnerViewSet) \
    .register(r'products', product_views.ProductViewSet,
              basename='partner-product', parents_query_lookups=['stockrecords__partner_id'])
router.register(r'products', product_views.ProductViewSet, basename='product')
router.register(r'vouchers', voucher_views.VoucherViewSet, basename='vouchers')
router.register(r'stockrecords', stockrecords_views.StockRecordViewSet, basename='stockrecords')

urlpatterns += router.urls
urlpatterns = format_suffix_patterns(urlpatterns)
