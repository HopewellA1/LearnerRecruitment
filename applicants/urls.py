from django.contrib import admin
from django.urls import path
from . import views



urlpatterns = [
    path('', views.home, name="home"),
    path('admin/', admin.site.urls),
    path('LPO1/', views.LPO5, name="LPO5"),
    path('download_excel/<int:categoryId>/', views.download_excel, name='download_excel'),
    path('learnercategories', views.learnercategories, name="learnercategories"),
    path('categories/', views.categories, name="categories"),
    path('Learners/<int:categoryId>/', views.Learners, name="Learners"),
    path('editLearner/<int:learnerId>/', views.editLearner, name="editLearner"),
    path('learnerDetails/<int:learnerId>', views.learnerDetails, name="learnerDetails"),
    path('deleteLearner/<int:learnerId>', views.deleteLearner, name="deleteLearner"),
    path('save_excel_to_db', views.save_excel_to_db, name="save_excel_to_db"),
    path('save_excel_to_db', views.save_excel_to_db, name="save_excel_to_db"),
    path('help/', views.help, name="help")
   
]