from django.shortcuts import render
from .models import MenuItem, Order, OrderItem, Profile
from django.contrib.auth.models import User
from .forms import UserForm
from django.db.models import Q
from django.contrib.auth import authenticate, login, logout
from django.http import HttpResponseRedirect, HttpResponse
from django.urls import reverse
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import Group
from django.core.files.storage import FileSystemStorage
from django.contrib.auth.decorators import user_passes_test


def index(request):
    context = {
        "items": User.objects.filter(groups__name='provider'),
    }
    return render(request, "index.html", context)


def group_required(*group_names):
    """Requires user membership in at least one of the groups passed in."""
    def in_groups(u):
        if u.is_authenticated():
            if bool(u.groups.filter(name__in=group_names)) | u.is_superuser:
                return True
        return False

    return user_passes_test(in_groups, login_url='403')


@login_required
def addToCard(request, menu_id):
    if request.method == "POST":
        userId = request.user.id
        menuItem = MenuItem.objects.get(pk=menu_id)
        try:
            order = Order.objects.get(user__id=userId, isPaid=False)
        except Order.DoesNotExist:
            order = Order.create(user=request.user,
                                 sellerUser=menuItem.user,
                                 isPaid=False)
            order.save()

        orderItem = OrderItem.create(menuItem)
        orderItem.price = menuItem.price
        orderItem.menuItemName = menuItem.name
        orderItem.save()
        order.orderItems.add(orderItem)
        order.save()
        return HttpResponseRedirect('/')

    if request.method == "GET":
        menuItem = MenuItem.objects.get(pk=menu_id)
        context = {
            "menuItem": menuItem,
        }
        return render(request, "add-to-card.html", context)


def user_logout(request):
    logout(request)
    return HttpResponseRedirect('/')


def register(request):
    registered = False
    if request.method == 'POST':
        user_form = UserForm(data=request.POST)
        if user_form.is_valid():
            user = user_form.save()
            user.set_password(user.password)
            user.save()
            userType = request.POST.get('user_type', 'normal')
            my_group, c = Group.objects.get_or_create(name=userType)
            user.groups.add(my_group)
            user.save()
            profile = Profile.create(user=user)
            profile.save()
            registered = True
        else:
            print(user_form.errors)
    else:
        user_form = UserForm()
    return render(request, 'registration.html', {'user_form': user_form,
                                                 'registered': registered})


def user_login(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        user = authenticate(username=username, password=password)
        if user:
            if user.is_active:
                login(request, user)
                return HttpResponseRedirect('/dashboard')
            else:
                return HttpResponse("Your account is inactive.")
        else:
            return HttpResponse("Invalid login details given")
    else:
        return render(request, 'login.html', {})


def cart(request):
    if request.method == "POST":
        return HttpResponseRedirect('/')

    if request.method == "GET":
        try:
            order = Order.objects.all().get(user__id=request.user.id,
                                            isPaid=False)
            items = order.orderItems.all()
            total = 0

            for item in items:
                total += item.price
            if total == 0:
                context = {
                    "message": "Your cart is empty",
                }
                return render(request, "cart.html", context)
            else:
                context = {
                    "order": order,
                    "items": items,
                    "total": format(total, '.2f')
                }
                return render(request, "cart.html", context)
        except Order.DoesNotExist:
            context = {
                "message": "Your cart is empty",
            }
            return render(request, "cart.html", context)


def confirmOrder(request):
    if request.method == "POST":
        body_unicode = request.body.decode('utf-8')
        address = request.POST.get("address", "")
        name = request.POST.get("name", "")
        phone = request.POST.get("phone", "")
        order_id = request.POST.get("order_id", "")
        order = Order.objects.all().get(pk=order_id)
        order.address = address
        order.name = name
        order.phone = phone
        order.isPaid = True
        items = order.orderItems.all()
        total = 0
        for item in items:
            total += item.price
        order.totalPrice = total
        order.save()
        context = {
            "order": order
        }
        return render(request, "order-confirm-page.html", context)


def deleteMenuItem(reques, orderId, itemId):
    item = OrderItem.objects.get(pk=itemId)
    order = Order.objects.get(pk=orderId)
    order.orderItems.remove(item)
    order.save()
    return HttpResponseRedirect('/cart')


@login_required
def dashboard(request):
    if bool(request.user.groups.filter(name__in=["provider"])):
        context = {
        }
        return render(request, "dashboard/index.html", context)
    else:
        return HttpResponseRedirect('/')


def dashboardEdit(request):
    userId = request.user.id
    profile = Profile.objects.get(user__id=userId)
    if request.method == "GET":
        context = {
            "profile": profile
        }
        return render(request, "dashboard/edit.html", context)
    else:
        name = request.POST.get('name', '')
        address = request.POST.get('address', '')
        tel = request.POST.get('tel', '')
        bio = request.POST.get('bio', '')
        file = False
        if 'profileImage' in request.FILES:
            file = request.FILES['profileImage']
        if file:
            fs = FileSystemStorage()
            filename = fs.save(file.name, file)
            uploaded_file_url = fs.url(filename)
            profile.imagePath = uploaded_file_url
        profile.name = name
        profile.address = address
        profile.tel = tel
        profile.bio = bio
        profile.save()
        return HttpResponseRedirect('/dashboard')


def dashboardMenu(request):
    userId = request.user.id
    context = {
        "menuItems": MenuItem.objects.filter(user__id=userId)
    }
    return render(request, "dashboard/menu.html", context)


def dashboardOrders(request):
    context = {
        "orders": Order.objects.filter(sellerUser__id=request.user.id,
                                       isAccepted=False,
                                       isRejected=False),
        "pastOrders": Order.objects.filter(Q(isAccepted=True) |
                                           Q(isRejected=True),
                                           sellerUser__id=request.user.id)
    }
    return render(request, "dashboard/orders.html", context)


def dashboarDeleteMenuItem(request, itemId):
    item = MenuItem.objects.get(pk=itemId, user__id=request.user.id)
    if item:
        item.delete()
    return HttpResponseRedirect('/dashboard/menu')


def dashboarAddItem(request):
    if request.method == "POST":
        name = request.POST.get('name', '')
        price = request.POST.get('price', '')
        desc = request.POST.get('desc', '')
        menuItem = MenuItem.create(request.user, name, price, desc)
        menuItem.save()
        return HttpResponseRedirect('/dashboard/menu')


def dashboardAcceptOrder(request, orderId):
    order = Order.objects.get(pk=orderId)
    order.isAccepted = True
    order.save()
    return HttpResponseRedirect('/dashboard/orders')


def dashboardRejectOrder(request, orderId):
    order = Order.objects.get(pk=orderId)
    order.isRejected = True
    order.save()
    return HttpResponseRedirect('/dashboard/orders')


def viewProfile(request, profileId):
    profile = Profile.objects.get(pk=profileId)
    profile.rate = round(profile.rate, 1)
    context = {
        "profile": profile,
        "menuItems": MenuItem.objects.filter(user__id=profile.user.id),
        "reviewCount": Order.objects.filter(Q(isAccepted=True) |
                                            Q(isRejected=True),
                                            sellerUser__id=profile.user.id,
                                            rate__isnull=False).count()
    }
    return render(request, "profile.html", context)


def giveFeedback(request):
    if request.method == "GET":
        orders = Order.objects.filter(Q(isAccepted=True) |
                                      Q(isRejected=True),
                                      user__id=request.user.id,
                                      rate__isnull=True)
        context = {
            "orders": orders
        }
        return render(request, "give-feedback.html", context)
    if request.method == "POST":
        orderId = request.POST.get('orderId', '')
        order = Order.objects.get(pk=orderId)
        order.rate = request.POST.get('rate', '')
        order.save()
        allFeedbacks = Order.objects.filter(Q(isAccepted=True) |
                                            Q(isRejected=True),
                                            sellerUser__id=order.sellerUser.id,
                                            rate__isnull=False)
        count = 0
        total = 0
        for feedback in allFeedbacks:
            total += feedback.rate
            count += 1
        if count != 0:
            average = total / count
        else:
            average = 2
        order.sellerUser.profile.rate = average
        order.sellerUser.profile.save()
        return HttpResponseRedirect('/give-feedback')
