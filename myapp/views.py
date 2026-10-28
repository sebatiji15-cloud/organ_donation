from django.shortcuts import render, redirect
from django.db import IntegrityError, models
from .models import UserRegistrations, HOSPITALRegistrations, Donations, OrganRequest

def index(request):
    return render(request, "index.html")

def reg(request):
    error = None
    if request.method == "POST":
        name = request.POST.get('username', '').strip()
        email = request.POST.get('email', '').strip()
        phno = request.POST.get('phonenumber', '').strip()
        blood = request.POST.get('blood', '').strip()
        pwd = request.POST.get('password', '').strip()

        if not name or not pwd or not email:
            error = "Please fill in all required fields."
        elif UserRegistrations.objects.filter(username=name).exists():
            error = f"Username '{name}' is already taken. Please choose another."
        else:
            try:
                reg_obj = UserRegistrations(username=name, email=email, blood=blood, phno=phno, password=pwd, rights='User')
                reg_obj.save()
                return redirect('/log/?registered=1')
            except IntegrityError:
                error = "An account with these details already exists."
            except Exception as e:
                error = f"Error during registration: {str(e)}"
    return render(request, "reg.html", {'error': error})

def log(request):
    error = None
    registered = request.GET.get('registered') == '1'
    if request.method == "POST":
        username = request.POST.get('username', '').strip()
        password = request.POST.get('password', '').strip()
        
        user_match = UserRegistrations.objects.filter(username=username, password=password).first()
        hos_match = HOSPITALRegistrations.objects.filter(username=username, password=password).first()

        if user_match:
            rights = user_match.rights
            request.session['role'] = rights
            request.session['username'] = user_match.username
            request.session['email'] = user_match.email
            request.session['blood'] = user_match.blood or ''
            
            if rights == "User":
                return redirect("/user/")
            elif rights == "Admin":
                return redirect("/adminp/")
            else:
                return redirect("/user/")
        elif hos_match:
            rights = hos_match.rights
            if rights == "Hospital":
                request.session['role'] = "Hospital"
                request.session['username'] = hos_match.username
                request.session['id'] = hos_match.id
                request.session['email'] = hos_match.emailid
                request.session['hospitalname'] = hos_match.hospitalname
                return redirect("/hospitalindex/")
            elif rights == "New Hospital":
                error = "Your hospital registration is currently pending Administrator approval."
            elif rights == "Rejected":
                error = "Your hospital registration has been rejected. Please contact the administrator."
            else:
                error = "Your hospital account status does not allow login."
        else:
            error = "Invalid username or password."
            try:
                import pyttsx3
                engine = pyttsx3.init()
                engine.say("invalid email or password")
                engine.runAndWait()
            except Exception:
                pass

    return render(request, "log.html", {'error': error, 'registered': registered})

def logout_view(request):
    request.session.flush()
    return redirect('/log/')

def hosreg(request):
    error = None
    success = None
    if request.method == "POST":
        name = request.POST.get('name', '').strip()
        username = request.POST.get('username', '').strip()
        address = request.POST.get('address', '').strip()
        emailid = request.POST.get('emailid', '').strip()
        phonenumber = request.POST.get('phonenumber', '').strip()
        password = request.POST.get('password', '').strip()

        if not name or not username or not password:
            error = "Please fill in all required fields."
        elif HOSPITALRegistrations.objects.filter(username=username).exists():
            error = f"Hospital username '{username}' is already registered."
        else:
            try:
                hos_obj = HOSPITALRegistrations(
                    hospitalname=name,
                    username=username,
                    address=address,
                    emailid=emailid,
                    phonenumber=phonenumber,
                    password=password,
                    rights='New Hospital'
                )
                hos_obj.save()
                success = "Hospital registered successfully! Your account will be activated once approved by the Admin."
            except Exception as e:
                error = f"Registration error: {str(e)}"
    return render(request, "hosreg.html", {'error': error, 'success': success})

def user(request):
    if 'email' not in request.session:
        return redirect('/log/')
    return render(request, "user.html", {
        'username': request.session.get('username', 'User'),
        'email': request.session.get('email', '')
    })

def admin(request):
    total_donations = Donations.objects.count()
    pending_donations = Donations.objects.filter(status__iexact='pending').count()
    approved_donations = Donations.objects.filter(status__iexact='Approved').count()
    
    total_requests = OrganRequest.objects.count()
    pending_requests = OrganRequest.objects.filter(status__iexact='Pending').count()
    approved_requests = OrganRequest.objects.filter(status__iexact='Approved').count()
    
    approved_hospitals = HOSPITALRegistrations.objects.filter(rights='Hospital').count()
    pending_hospitals = HOSPITALRegistrations.objects.filter(rights='New Hospital').count()
    total_users = UserRegistrations.objects.filter(rights='User').count()

    recent_donations = Donations.objects.all().order_by('-id')[:6]
    recent_requests = OrganRequest.objects.all().order_by('-id')[:6]
    pending_hospitals_list = HOSPITALRegistrations.objects.filter(rights='New Hospital').order_by('-id')[:5]

    context = {
        'total_donations': total_donations,
        'pending_donations': pending_donations,
        'approved_donations': approved_donations,
        'total_requests': total_requests,
        'pending_requests': pending_requests,
        'approved_requests': approved_requests,
        'approved_hospitals': approved_hospitals,
        'pending_hospitals': pending_hospitals,
        'total_users': total_users,
        'recent_donations': recent_donations,
        'recent_requests': recent_requests,
        'pending_hospitals_list': pending_hospitals_list,
    }
    return render(request, "admin.html", context)

def newhospital(request):
    hos = HOSPITALRegistrations.objects.filter(rights='New Hospital')
    return render(request, "newhospital.html", {'hos': hos})

def app_hospital(request, id):
    HOSPITALRegistrations.objects.filter(id=id).update(rights="Hospital")
    return redirect('/newhospital/')

def rej_hospital(request, id):
    HOSPITALRegistrations.objects.filter(id=id).update(rights='Rejected')
    return redirect('/newhospital/')

def hospitals(request):
    hos = HOSPITALRegistrations.objects.filter(rights='Hospital')
    return render(request, "hospitals.html", {'hos': hos})

def addorgan(request):
    if 'email' not in request.session:
        return redirect('/log/')
    user_email = request.session['email']
    hst = HOSPITALRegistrations.objects.filter(rights="Hospital")
    if request.method == "POST":
        name = request.POST.get('name')
        emailid = request.POST.get('email')
        address = request.POST.get('address')
        bloodgroup = request.POST.get('bloodgroup')
        organtype = request.POST.get('organtype')
        age = request.POST.get('age')
        hospital = request.POST.get('hospital')
        reg_obj = Donations(
            user=user_email,
            name=name,
            email=emailid,
            address=address,
            bloodgroup=bloodgroup,
            organtype=organtype,
            age=age,
            hospital=hospital,
            status="pending"
        )
        reg_obj.save()
        return redirect('/organdonate/')
    return render(request, "addorgan.html", {'hst': hst})

def organdonate(request):
    if 'email' not in request.session:
        return redirect('/log/')
    email = request.session['email']
    don = Donations.objects.filter(user=email).order_by('-id')
    return render(request, "organdonate.html", {'don': don})

def hospitalindex(request):
    if 'id' not in request.session and request.session.get('role') != 'Hospital':
        return redirect('/log/')
    return render(request, "hospitalindex.html", {
        'hospitalname': request.session.get('hospitalname', 'Hospital')
    })

def neworgandonation(request):
    role = request.session.get('role', '')
    if role == 'Admin':
        don = Donations.objects.all().order_by('-id')
        is_admin = True
    elif 'id' in request.session:
        ids = request.session['id']
        hos_obj = HOSPITALRegistrations.objects.filter(id=ids).first()
        hos_name = hos_obj.hospitalname if hos_obj else ''
        don = Donations.objects.filter(
            models.Q(hospital=str(ids)) | models.Q(hospital__iexact=hos_name)
        ).order_by('-id')
        is_admin = False
    else:
        return redirect('/log/')
    return render(request, "neworgandonation.html", {'don': don, 'is_admin': is_admin})

def app_user(request, id):
    Donations.objects.filter(id=id).update(status="Approved")
    return redirect('/neworgandonation/')

def rej_user(request, id):
    Donations.objects.filter(id=id).update(status='Rejected')
    return redirect('/neworgandonation/')

def organrequest(request):
    if 'email' not in request.session:
        return redirect('/log/')
    email = request.session['email']
    req = OrganRequest.objects.filter(email=email).order_by('-id')
    return render(request, "organrequest.html", {'req': req, 'is_admin': False})

def deleterequest(request, id):
    OrganRequest.objects.filter(id=id).delete()
    return redirect('/admareq/')

def approverequest(request, id):
    OrganRequest.objects.filter(id=id).update(status='Approved')
    return redirect('/admareq/')

def odreg(request):
    if 'email' not in request.session:
        return redirect('/log/')
    if request.method == "POST":
        username = request.POST.get('username')
        email = request.POST.get('email')
        address = request.POST.get('address')
        age = request.POST.get('age')
        bloodgroup = request.POST.get('bloodgroup')
        organtype = request.POST.get('organtype')
        gender = request.POST.get('gender')
        phonenumber = request.POST.get('phonenumber')
        reg_obj = OrganRequest(
            username=username,
            email=email,
            address=address,
            age=age,
            bloodgroup=bloodgroup,
            organtype=organtype,
            gender=gender,
            phonenumber=phonenumber,
            status='Pending'
        )
        reg_obj.save()
        return redirect('/organrequest/')
    return render(request, "odreg.html", {
        'initial_username': request.session.get('username', ''),
        'initial_email': request.session.get('email', '')
    })

def orhistory(request):
    blood = request.session.get('blood', '')
    if blood:
        req = OrganRequest.objects.filter(bloodgroup__iexact=blood, status='Approved').order_by('-id')
        if not req.exists():
            req = OrganRequest.objects.filter(status='Approved').order_by('-id')
    else:
        req = OrganRequest.objects.filter(status='Approved').order_by('-id')
    return render(request, "orhistory.html", {'req': req, 'blood': blood})

def hosoreq(request):
    req = OrganRequest.objects.all().order_by('-id')
    return render(request, "hosoreq.html", {'req': req})

def admareq(request):
    req = OrganRequest.objects.all().order_by('-id')
    return render(request, "organrequest.html", {'req': req, 'is_admin': True})

def userprof(request):
    if 'email' not in request.session:
        return redirect('/log/')
    email = request.session['email']
    success = False
    if request.method == "POST":
        name = request.POST.get('username')
        phno = request.POST.get('phonenumber')
        pwd = request.POST.get('password')
        UserRegistrations.objects.filter(email=email).update(username=name, phno=phno, password=pwd)
        request.session['username'] = name
        success = True
    re = UserRegistrations.objects.filter(email=email)
    return render(request, "userprof.html", {'re': re, 'success': success})

def hosprof(request):
    if 'email' not in request.session:
        return redirect('/log/')
    emailid = request.session['email']
    success = False
    if request.method == "POST":
        name = request.POST.get('hospitalname')
        username = request.POST.get('username')
        address = request.POST.get('address')
        phno = request.POST.get('phonenumber')
        pwd = request.POST.get('password')
        HOSPITALRegistrations.objects.filter(emailid=emailid).update(
            hospitalname=name,
            username=username,
            address=address,
            phonenumber=phno,
            password=pwd
        )
        if name:
            request.session['hospitalname'] = name
        if username:
            request.session['username'] = username
        success = True
    ed = HOSPITALRegistrations.objects.filter(emailid=emailid)
    return render(request, "hosprof.html", {'ed': ed, 'success': success})
