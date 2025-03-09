def detect(user):
    if user.type==1:
        redirect_url='vendorDashboard'
        return redirect_url
    elif user.type==2:
        redirect_url='customerDashboard'
        return redirect_url
    elif user.type==None and user.is_superadmin:
        redirect_url='/admin'
        return redirect_url
    