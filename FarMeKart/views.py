from django.shortcuts import render,redirect
from FarMeKart.forms import UsregFo,ChpwdForm,UpdPfle,Vegfr,UpdVgtab,Userp,Usperm,UpdPfle1,CancelForm,UpdPfle2,PlaceorderForm
from django.contrib.auth.decorators import login_required
from farmer import settings
from django.core.mail import send_mail
from django.core.mail import EmailMessage
from django.contrib.auth.models import User,AbstractUser
from FarMeKart.models import Vegpro,User,Cart,Myorders
import sys
import secrets
from django.http import HttpResponse

# Create your views here.






def remove(request,id):
	c=Cart.objects.get(id=id)
	c.delete()
	return redirect('/cartdetails')

	

def contact(re):
	return render(re,"html/contact.html")

def about(re):
	return render(re,"html/about.html")

def registration(request):
	if request.method=="POST":
		k = UsregFo(request.POST)
		if k.is_valid():
			e = k.save(commit=False)
			e.idgen = secrets.token_hex(3)
			sb = "FarMeKart"
			mg = "Hi Welcome{}. You have successfully registered for FarMeKart portal. Your id is {}.".format(e.username,e.idgen)
			sd = settings.EMAIL_HOST_USER
			snt = send_mail(sb,mg,sd,[e.email])
			if snt == 1:
				e.save()
				return redirect('/lg')
			else:
				return redirect('/')
	k=UsregFo()
	return render(request,'html/register.html',{'h':k})

@login_required
def cgf(re):
	if re.method=="POST":
		c=ChpwdForm(user=re.user,data=re.POST)
		if c.is_valid():
			c.save()
			return redirect('lg/')
	c=ChpwdForm(user=re.user)
	return render(re,'html/changepassword.html',{'t':c})

@login_required
def profile(req):
	return render(req,'html/profile.html')

@login_required
def updprofile(request):
	if request.method == "POST":
		t = UpdPfle(request.POST,instance=request.user)
		if t.is_valid():
			t.save()
			return redirect('/pro')
	t = UpdPfle(instance=request.user)
	return render(request,'html/updateprofile.html',{'z':t})


@login_required
def dashboard(re):
	return render(re,'html/dashboard.html')

@login_required
def farmerdashboard(request):
	return render(request,'html/farmerdashboard.html')


@login_required
def vegf(request):
	t = Vegpro.objects.filter(a_id=request.user.id)
	if request.method == "POST":
		s = Vegfr(request.POST,request.FILES)
		if s.is_valid():
			r = s.save(commit=False)
			r.a_id = request.user.id
			r.save()
			return redirect('/dt')
	s=Vegfr()
	return render(request,'html/data.html',{'a':s,'e':t})

def home(re):
	i = Vegpro.objects.filter(a_id=re.user.id)
	s = Vegpro.objects.all() 
	k = {}
	for m in s:
		g = User.objects.get(id=m.a_id)
		k[m.id] = m.item_type,m.item_name,m.quantity,m.price,m.impf,m.is_stock,m.create_date,g.username
	f = k.values()
	return render(re,'html/user.html',{'it':i,'d':f})


@login_required
def infodelete(req,et):
	data=Vegpro.objects.get(id=et)
	print(data.id)
	if req.method == "POST":
		print(data.id)
		data.delete()
		return redirect('/dt')
	return render(req,'html/userdelete.html',{'sd':data})

def itemupdate(request,y):
	dc = Vegpro.objects.get(id=y)
	if request.method == "POST":
		m = UpdVgtab(request.POST,request.FILES,instance=dc)
		if m.is_valid():
			m.save()
			return redirect('/dt')
	m = UpdVgtab(instance=dc)
	return render(request,'html/updateuser.html',{'e':m})






def items(request):
	i = Vegpro.objects.filter(a_id=request.user.id)
	data=Vegpro.objects.all()
	for j in i:
		print(j.item_name)
	s = Vegpro.objects.all()
	k = {}
	for m in s:
		g = User.objects.get(id=m.a_id)
		k[m.id] = m.item_type,m.item_name,m.quantity,m.price,m.impf,m.market_price,m.is_stock,m.create_date,g.username
	f = k.values()
	return render(request,'html/cart.html',{'data':data,'d':f})

def addcart(request,id):
	r=Vegpro.objects.get(id=id)
	if request.method == 'POST': 
		p=Cart(user_id=request.user.id,veg_id=id)
		p.save()
		
		return redirect("/cartdetails")
	
	return render(request,'html/cart.html',{'data':r})

def usr(re):
	s=Userp()
	return render(re,'html/user.html',{'a':s})
def requestform(request):
	if request.method=="POST":
		u=request.POST.get('uname')
		e=request.POST.get('email')
		ut=request.POST.get('utype')
		ud=request.POST.get('uid')
		ms=request.POST.get('msg')
		f=request.FILES['fe']
		a="Hi welcome "+u+"<br/>" "Requested your Role as "+ut+"<br/>" "Your ID is:"+ud
		t = EmailMessage("UserRole Change",a,settings.EMAIL_HOST_USER,[settings.ADMINS[0][1],e])
		t.content_subtype='html'
		t.attach(f.name,f.read(),f.content_type)
		t.send()
		if t==1:
			return redirect('/reqp')
		else:
			return redirect('/lg')
	return render(request,'html/requestp.html')



def adminpermissions(request):
	ty=User.objects.all()
	return render(request,'html/adminpermissions.html',{'q':ty})
def updatepermissions(request,k):
	r=User.objects.get(id=k)
	if request.method == "POST":
		k=Usperm(request.POST,instance=r)
		if k.is_valid():
			k.save()
			return redirect('/gper')
	k2= Usperm(instance=r)
	return render(request,'html/updatepermissions.html',{'y':k2})

def updateprofile(request):
	return render(request,'html/profileupdate.html')

def orgupdate(request):
	z=User.objects.get(id=request.user.id)
	if request.method == "POST":
		p=UpdPfle1(request.POST,instance=z)
		q=UpdPfle2(request.POST,instance=z)
		r=UpdPfle(request.POST,instance=z)
		if p.is_valid() and q.is_valid() and r.is_valid():
			p.save()
			q.save()
			r.save()
			return redirect('/profile')
	p=UpdPfle1(instance=z)
	q=UpdPfle2(instance=z)
	r=UpdPfle(instance=z)
	return render(request,'html/updatedetails.html',{'u':p,'p':q,'k':r})

def userdelete(request,id):
	c=User.objects.get(id=id)
	c.delete()
	c.save()
	return redirect('/gper')

def addcart(request,id):
	b=Vegpro.objects.get(id=id)
	print("hi")
	print(b)

	c=Cart(user_id=request.user.id,veg_id=id)
	c.save()
	count=0
	data1 = Cart.objects.filter(user_id=request.user.id)
	for i in data1:
		count+=1
	return render(request,'html/addcart.html',{'b':c,'count':count,'data1':data1})

def cartdetails(request):
	c=Cart.objects.filter(user_id=request.user.id)
	sum=0
	count=0
	for i in c:
		count=count+1
		sum=sum+(i.veg.price)
	return render(request,'html/cartdetails.html',{'sum':sum,'count':count,'cart':c})

def placeorder(request):
	c=Cart.objects.filter(user_id=request.user.id)
	sum=0
	count=0
	for i in c:
		count=count+1
		sum=sum+i.veg.price
	return render(request,'html/placeorder.html',{'sum':sum,'count':count,'cart':c})

def msg(request):
	c=Cart.objects.filter(user_id=request.user.id)
	sum=0
	count=0
	for i in c:
		count=count+1
		sum=sum+i.veg.price
	return render(request,'html/message.html',{'count':count})


def msg1(request):
	c=Cart.objects.filter(user_id=request.user.id)
	sum=0
	count=0
	for i in c:
		count=count+1
		sum=sum+i.veg.price
	return render(request,'html/message1.html',{'count':count})

def msg2(request):
	
	return render(request,'html/msg2.html')


def myorders(request):
	my=Myorders.objects.filter(user_id=request.user.id)
	sum=0
	count=0
	for i in my:
		count=count+1
		sum=sum+i.price
	return render(request,'html/myorders.html',{'sum':sum,'my':my})


def checkout(request):
	c=Cart.objects.filter(user_id=request.user.id)
	
	if request.method=="POST":
		m=request.user.email
		receiver=m
		l=[]
		x=[]
		sum=0
		for i in c:
			sum=sum+i.veg.price
			l.append(i.veg.item_name)
				
		message='Ordered items ::\n'+' ,'.join(l)+'\n'+ 'will be delivered within 15 days.\n'+'Total amount paid: Rs.'+str(sum)+'\n'+'THANK YOU for Shopping!! \n'
		subject='Order confirmed'
		st=settings.EMAIL_HOST_USER
		if c:
			at=send_mail(subject,message,st,[receiver])
				
			for i in x:
				at.attach(i.name,i.read())
				at.send()
			for i in c:
				sum=sum+i.veg.price
				a=Myorders(item_name=i.veg.item_name,price=i.veg.price,user_id=request.user.id)
				a.save()
				he=Vegpro.objects.filter(id=i.veg_id)
				for i in he:
					i.save()
			c.delete()
			return redirect('msg')
		return redirect('msg1')
		
	
	return render(request,'html/placeorder.html')
	
def ordercancel(request,si):
	x=Myorders.objects.get(id=si)
	j=CancelForm(request.POST,instance=x)
	if request.method=="POST":
		if j.is_valid():
			receiver=request.user.email
			sender=settings.EMAIL_HOST_USER
			subject="order cancelled"
			body="your order has been cancelled"
			send_mail(sender,body,subject,[receiver])
			j.save()
			return redirect('msg2')
			he=Product.objects.filter(id=i.product_id)
			for i in he:
				i.totalquantity+=1
				i.save()
		x.delete()
	j=CancelForm(instance=x)
	return render(request,'html/ordercancel.html',{'prod':j})

