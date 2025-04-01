from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.models import User
from .models import Fertilizer, P_profile
from django.db.models import Q
from .forms import FertilizerForm, P_profileForm
from scipy.optimize import minimize

# Create your views here.

def home(request):
    return render(request, 'main/home.html')

def user_login(request):
    er = {'error': None}
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            return redirect('home')
        else:
            er['error'] = "Неверный логин или пароль"
    return render(request, 'main/login.html', er)

def user_logout(request):
    logout(request)
    return redirect('home')

def user_reg(request):
    er = {'error': None}
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        password2 = request.POST['password2']
        if password == password2:
            if not User.objects.filter(username=username).exists():
                user = User.objects.create_user(username=username, password=password)
                login(request, user)
                return redirect('home')
            else:
                er['error'] = "Пользователь с таким логином уже существует"
        else:
            er['error'] = "Пароли не совпадают"
    return render(request, 'main/reg.html', er)

def profile(request):
    if request.user.is_authenticated:
        fertilizers = Fertilizer.objects.filter(Q(user = request.user))
        return render(request, 'main/profile.html', {'fertilizers': fertilizers})
    else:
        return redirect('home')

def profile_pp(request):
    if request.user.is_authenticated:
        p_profile = P_profile.objects.filter(Q(user = request.user))
        return render(request, 'main/profile_pp.html', {'p_profiles': p_profile})
    else:
        return redirect('home')
    
def delete_fertilizer(request, pk):
    get_object_or_404(Fertilizer, pk=pk).delete()
    return redirect('profile')

def add_fertilizer(request):
    if request.method == 'POST':
        form = FertilizerForm(request.POST)
        if form.is_valid():
            fertilizer = form.save(commit=False)
            fertilizer.user = request.user
            fertilizer.save()
            return redirect('profile')
    else:
        form = FertilizerForm()
    return render(request, 'main/add_fertilizer.html', {'form': form})

def edit_fertilizer(request, pk):
    fertilizer = get_object_or_404(Fertilizer, pk=pk)
    if request.method == 'POST':
        form = FertilizerForm(request.POST, instance=fertilizer)
        if form.is_valid():
            form.save()
            return redirect('profile')
    else:
        form = FertilizerForm(instance=fertilizer)
    return render(request, 'main/add_fertilizer.html', {'form': form})

def delete_p_profile(request, pk):
    get_object_or_404(P_profile, pk=pk).delete()
    return redirect('profile_pp')

def add_p_profile(request):
    if request.method == 'POST':
        form = P_profileForm(request.POST)
        if form.is_valid():
            p_profile = form.save(commit=False)
            p_profile.user = request.user
            p_profile.save()
            return redirect('profile_pp')
    else:
        form = P_profileForm()
    return render(request, 'main/add_p_profile.html', {'form': form})

def edit_p_profile(request, pk):
    p_profile = get_object_or_404(P_profile, pk=pk)
    if request.method == 'POST':
        form = P_profileForm(request.POST, instance=p_profile)
        if form.is_valid():
            form.save()
            return redirect('profile_pp')
    else:
        form = P_profileForm(instance=p_profile)
    return render(request, 'main/add_p_profile.html', {'form': form})

def calc(request):
    if request.user.is_authenticated:
        fertilizers = Fertilizer.objects.filter(Q(user=request.user) | Q(is_public=True))
        p_profiles = P_profile.objects.filter(Q(user=request.user) | Q(is_public=True))
    else:
        fertilizers = Fertilizer.objects.filter(Q(is_public=True))
        p_profiles = P_profile.objects.filter(Q(is_public=True))
    names = []
    answer = []
    er=""
    profile=[]
    el_names=[]
    if request.method == 'POST':
        selected_fertilizers = Fertilizer.objects.filter(id__in=request.POST.getlist('fertilizers'))
        selected_profile = get_object_or_404(P_profile, id=request.POST.get('p_profile'))

        if selected_fertilizers:
            f = []
            profile = list(vars(selected_profile).values())[5:]
            el_names = list(vars(selected_profile).keys())[5:]
            for i in range(8):
                profile[i+8] = profile[i+8] * 0.001

            for fertilize in selected_fertilizers:
                new_f = vars(fertilize)
                new_f['p2o5']=new_f['p2o5'] * 0.436
                new_f['k2o']=new_f['k2o'] * 0.83
                new_f['cao']=new_f['cao'] * 0.715
                new_f['mgo']=new_f['mgo'] * 0.603
                names.append(list(new_f.values())[4])
                f.append(list(new_f.values())[5:])

            def mix(doses, f):
                result = [0]*16
                for i in range(len(doses)):
                    for k in range(16):
                        result[k]+=(doses[i]*f[i][k])/100
                return result

            def func(doses, f, profile):
                fault = 0.05
                res = mix(doses, f)
                penalty = 0
                covered = 0
                for i in range(len(profile)):
                    if profile[i] > 0:
                        if abs(res[i]-profile[i])/profile[i] <= fault:
                            covered += 1
                        elif res[i] > profile[i]:
                            penalty += ((res[i] - profile[i]) ** 2) * (0.5+((1-(i//8))*0.5))
                        else:
                            penalty += (profile[i] - res[i]) * (0.5+((1-(i//8))*0.5))
                return penalty - (covered*(1/16)*penalty)
            
            start_doses = [0] * len(selected_fertilizers)
            bounds = [(0, None) for _ in range(len(selected_fertilizers))]

            answer = minimize(func, start_doses, args=(f, profile), bounds=bounds, method='L-BFGS-B').x 
            answer = list(map(lambda x: round(x), answer))

            for k in range(16):
                for i in range(len(selected_fertilizers)):
                    profile[k] -= (f[i][k]*answer[i])/100
            profile = list(map(lambda x: round(x), profile))

        else:
            er = "Выберите хотя бы 1 удобрение"

        
    return render(request, 'main/calc.html', {'fertilizers': fertilizers, 'p_profiles': p_profiles, 'answer': dict(zip(names, answer)), 'er': er, 'res': dict(zip(el_names, profile))})

def calc_p_profile(request):
    start_profile = {
      "N": 100,
      "P": 20,
      "K": 50,
      "Ca": 60,
      "Mg": 25,
      "S": 15
    }
    return render(request, "main/calc_p_profile.html", {"macros": start_profile})