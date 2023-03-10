from django.urls import path
from  . import views

urlpatterns =[
    path('coalstock/',views.coalspec_list, name = 'coalstockforblending'),
    path('blending/',views.calculate_blending, name = 'calculateblending'),
    path('blending/history',views.search_history, name= 'searchhistory'),
    path('blending/resumehistory',views.search_resume_history, name= 'searchresumehistory'),
    path('note/',views.create_note, name = 'createnote'),

    path('blending/prep',views.prepare_for_blend, name = 'prepareblending'),


]