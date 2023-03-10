from django.urls import path
from  . import views
from django.conf.urls.static import static
from django.conf import settings

urlpatterns =[

    path ('ub/',views.create_ub,name ='createub'),
    path ('ub/<id>/view',views.view_unitboiler, name ='viewunit'),
    path ('ub/list',views.list_ub,name ='listunitboiler'),
    path('ub/<id>/updateub',views.update_unitboiler, name = 'updateunit'),
    path('ub/<id>/deleteub',views.delete_unitboiler, name = 'deleteunit'),

    path('roh/',views.set_rohunit_fromfile, name = 'setroh'),
    path('roh/template',views.roh_csv, name = 'rohtemplate'),

    path('hpbb/', views.createHargaPerkiraanBB, name ='createhpbb'),
    path('hpbb/<id>/deletehp', views.deleteHargaPerkiraanBB, name ='deletehpbb'),
    path('hpbb/<id>/edithp', views.editHargaPerkiraanBB, name ='edithpbb'),

    path('fromfile/', views.set_param_fromfile,name = 'unggahparam'),
    path('fromfile/', views.download,name = 'downloadtemp'),

    path('optbeban/',views.create_prm_opt_beban, name= 'prmoptbeban'),
    path('optbeban/list',views.parameteroptbebanlist, name= 'prmoptbebanlist'),
    path('optbeban/<unit>',views.prm_opt_beban_view, name= 'detailpoptbunit'),
    path('optbeban/<unit>/updateoptb',views.update_paramoptb, name= 'updateppoptbunit'),
    path('optbeban/<unit>/deleteoptb',views.delete_parameteroptb, name= 'deletepoptbunit'),


    path('optblending/',views.create_prm_opt_blending, name = 'createprmblending'),
    path('optblending/list',views.parameterblendinglist, name = 'parameterblendinglist'),
    path('optblending/<unit>',views.parameterblending_view, name = 'detailpbunit'),
    path('optblending/<unit>/updatepb',views.parameterblending_update, name = 'updatepbunit'),
    path('optblending/<unit>/deletepb',views.delete_parameterblending, name = 'deletepbunit'),



]

if settings.DEBUG:
        urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)