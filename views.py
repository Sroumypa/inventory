from django.shortcuts import render
from .forms import UserLoginForm

from .models import Inventory, Userp, Role
from django.contrib.auth import authenticate
from django.contrib.auth.models import User
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status, permissions

from .serializers import InventorySerializer


class LoginView(APIView):
    def User_login(request):
        if request.method == "POST":
            form = UserLoginForm(request.POST)
            if form.is_valid:
                username = request.POST["Username"]
                password = request.POST["Password"]
                user = authenticate(username=username, password=password)
                if user:
                    if user.is_active:
                        login(request, user)
                        messages.success(request, "user logged in successfully")
                        return redirect("Post_List")
                    else:
                        return HttpResponse("User is Not Active")
                else:
                    return HttpResponse("User is None")
            else:
                return HttpResponse("User is not valid")

        else:
            form = UserLoginForm()
            return render(request, "login.html", {"form": form})


class InventoryView(APIView):
    permission_classes = [permissions.IsAuthenticated]

    def post(self, request):
        # Check if the user has permission to add inventory (Department Manager)
        user_profile = Userp.objects.get(user=request.user)
        if 'Department Manager' not in user_profile.roles.values_list('name', flat=True):
            return Response({'success': False, 'error': 'Permission denied'}, status=status.HTTP_403_FORBIDDEN)

        serializer = InventorySerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response({'success': True, 'message': 'Inventory record(s) added successfully'})
        else:
            return Response({'success': False, 'error': serializer.errors}, status=status.HTTP_400_BAD_REQUEST)

    def get(self, request):
        # Check if the user has permission to fetch inventory
        user_profile = Userp.objects.get(user=request.user)
        if 'Department Manager' in user_profile.roles.values_list('name', flat=True) or \
                'Store Manager' in user_profile.roles.values_list('name', flat=True):
            inventory_records = Inventory.objects.all()
            serializer = InventorySerializer(inventory_records, many=True)
            return Response({'success': True, 'inventory': serializer.data})
        else:
            return Response({'success': False, 'error': 'Permission denied'}, status=status.HTTP_403_FORBIDDEN)

    def put(self, request):
        # Check if the user has permission to approve inventory (Store Manager)
        user_profile = Userp.objects.get(user=request.user)
        if 'Store Manager' not in user_profile.roles.values_list('name', flat=True):
            return Response({'success': False, 'error': 'Permission denied'}, status=status.HTTP_403_FORBIDDEN)

        inventory_ids_to_approve = request.data.get('inventory_ids')
        if not inventory_ids_to_approve:
            return Response({'success': False, 'error': 'No inventory records to approve'},
                            status=status.HTTP_400_BAD_REQUEST)

        try:
            inventory_records = Inventory.objects.filter(id__in=inventory_ids_to_approve)
            for record in inventory_records:
                record.status = 'Approved'
                record.save()

            return Response({'success': True, 'message': 'Inventory record(s) approved successfully'})
        except Inventory.DoesNotExist:
            return Response({'success': False, 'error': 'Invalid inventory record(s)'},
                            status=status.HTTP_400_BAD_REQUEST)