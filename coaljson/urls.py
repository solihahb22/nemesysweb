from django.urls import path
from  . import views
from .views import SelectCoalView
from django.contrib.auth import views as authview
from .forms import UserLoginForm
urlpatterns =[
    path('coal/',views.new_coal, name='new_coal'),
    path('coaljson/',views.new_coal_json, name='new_coal_json'),
    path('coalspec/', views.new_coal_spec,name='coalspeccreate'),
    path('coalspeclist/',views.coalspec_list, name='coalspeclist'),
    path('coalspeclistapi/', views.coalspecserializer_list, name ='coalspecapi'),
    # path('',authview.LoginView.as_view(
    #         template_name="login.html",
    #         authentication_form=UserLoginForm
    #         ),
    #     name='login'),

    path('',views.index, name = 'index'),
    path('coalstock/', views.new_coal_stock_unit, name='new_coal_stock'),
    path('coalstock/<unit>/listcsu', views.coal_stock_unit_list, name='coal_stock_unit_list'),
    path('coalstock/search', views.search_stock_unit, name='search_coal_stock_unit'),
    path('coalstock/search_old', views.search_stock_unit_old, name='search_coal_stock_unit_old'),
    path('coalstock/search_op', views.search_stock_unit_short, name='search_coal_stock_unit_short'),

    path('coalstock/<id>/updateunit', views.update_coal_stock_unit, name='updatecoalstock'),
    path('coalstock/<id>/updatesimple', views.update_stock_simple, name='simpleupdatecoal'),
    path('coalstock/<id>/update', views.update_stock_simple2, name='simpleupdatecoal2'),
    path('coalstock/delete/<id>', views.delete_coal_stock_unit, name='deletecoalstock'),
    path('coalstock/fromapi', views.coalstockfromapi, name='getcoalstockfromapi'),
    #path('coalstock/prep/', views.get_coal_for_blending, name='preparecoalforblending'),
    path('coalstock/prep/', views.get_coal_for_blending_op, name='preparecoalforblending'),
    path('coalstock/<unit>/list', views.view_coal_stock_unit, name='coal_stock_unit'),
    path('coalstock/temp/', views.generatebiofromtemp, name='generate_bio_from_temp'),

    path('coalstock/fromspecapi', views.get_coal_from_db, name='getcoalstockfromspecapi'),

    path('coalstock/bio', views.get_bio_for_blending, name='getbioforblend'),
    path('coalstock/bio/<int:bio_id>', views.select_bio_for_blending, name='selectbioforblend'),
    path('coalstock/tkg', views.get_coal_tk_for_blending, name='gettongkang'),
    path('coalstock/tk/<int:coaltk_id>', views.select_coal_tk_for_blending, name='selecttongkang'),
    path('coalstock/cyd', views.get_coal_cyrd_for_blending, name='getcoalyard'),
    path('coalstock/cyd/<int:cyrd_id>', views.get_coal_cyrd_for_blending, name='selectcoalyards'),
    path('coalstock/next', views.nextstep_setunit, name='nextstepsetunit'),
    path('coalstock/cyd/<int:cyrd_id>', views.submit_coal_for_blending, name='submitcoalforblend'),
    path('coalstock/select/<int:pk>', SelectCoalView.as_view(), name="selectcoal")








]