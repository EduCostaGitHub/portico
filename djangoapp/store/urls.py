from django.urls import path


from store.views import ProductList, ProductDetail, AddToCart, \
    RemoveFromCart, Cart, Resume, ProductSearch, \
    CreateProfile, UpdateProfile, LoginProfile, \
    LogoutProfile, RequestPay, RequestSave, RequestList, RequestDetail


app_name = 'store'

urlpatterns = [
    # profile
    path('profile/', CreateProfile.as_view(), name='profile_create'),
    path('profile/update/', UpdateProfile.as_view(), name='profile_update'),
    path('profile/login/', LoginProfile.as_view(), name='profile_login'),
    path('profile/logout/', LogoutProfile.as_view(), name='profile_logout'),

    # product
    path('', ProductList.as_view(), name='list'),
    path('addtocart/', AddToCart.as_view(), name='addtocart'),
    path('removefromcart/', RemoveFromCart.as_view(), name='removefromcart'),
    path('cart/', Cart.as_view(), name='cart'),
    path('resume/', Resume.as_view(), name='resume'),
    path('search/', ProductSearch.as_view(), name='search'),
    path('<slug>/', ProductDetail.as_view(), name='detail'),

    # request
    path('request/pay/<int:pk>', RequestPay.as_view(), name='request_pay'),
    path('request/save/', RequestSave.as_view(), name='request_save'),
    path('request/list/', RequestList.as_view(), name='request_list'),
    path('request/detail/<int:id>', RequestDetail.as_view(), name='request_detail'),

]
