from django.urls import path
from  . import views

urlpatterns =[

    #path('calculateoptb/',views.calc_optimasi_beban, name = 'calculateoptb'),
    path('calculateoptb/select',views.select_unit_optb, name = 'selectunitoptb'),
    path('calculateoptb/rk',views.calculate_rk_unit_update, name = 'calculate_rku'),
    path('calculateoptb/view_rk',views.view_rk_unit, name = 'view_rku'),
    path('calculateoptb/roh',views.unggah_roh_unit_harian, name = 'unggah_roh'),

]