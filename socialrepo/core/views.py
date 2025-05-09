from django.shortcuts import render,redirect
from django.http import HttpResponse
from django.contrib.auth.models import User,auth
from django.contrib import messages
from core.models import Profile,Post,LikePost,FollowersCount
from django.contrib.auth.decorators import login_required
from itertools import chain
# Create your views here.
@login_required(login_url='signin')
def index(request):
    
    user_object = User.objects.get(username=request.user.username)
    user_profile = Profile.objects.get(user=user_object)
    posts=Post.objects.all()
    return render(request,'core/index.html',{'posts':posts,"user_profile":user_profile})


@login_required(login_url='signin')
def upload(request):
    
    if request.method == 'POST':
        user = request.user.username
        image = request.FILES.get('image_upload')
        caption = request.POST['caption']

        new_post = Post.objects.create(user=user, image=image, caption=caption)
        new_post.save()

        return redirect('index')
    else:
        return redirect('index')
    
@login_required(login_url='signin')
def like_post(request):
    username=request.user.username
    post_id=request.GET.get('post_id')

    #fetch post object using post_id
    post=Post.objects.get(id=post_id)
   
    like_filter=LikePost.objects.filter(post_id=post_id,username=username).first()
    
    if like_filter is None:
        new_like=LikePost.objects.create(post_id=post_id,username=username)
        new_like.save()
        post.no_likes=post.no_likes+1
        post.save()
        return redirect('index')
    else:
        like_filter.delete()
        post.no_likes=post.no_likes-1
        post.save()
        return redirect('index')



def signup(req):
    if req.method=="POST":
        username=req.POST['username']
        email=req.POST['email']
        password=req.POST['password']
        password2=req.POST['password2']
        
        if password==password2:
            if User.objects.filter(email=email).exists():
                messages.info(req,"email has been already taken!")
                return redirect('signup')
            
            elif User.objects.filter(username=username).exists():
                messages.info(req,"username already taken!")
                return redirect('signup')
            
            else:
                #create new user
                user=User.objects.create_user(username=username,email=email,password=password2)
                user.save()
                # log user in and redirect to settings page
                user_login=auth.authenticate(username=username,password=password)
                auth.login(req,user_login)

                #create a profile object for the user    
                user_model=User.objects.get(username=username)
                new_profile=Profile.objects.create(user=user_model,id_user=user_model.id)
                new_profile.save()
                return redirect('settings')

        else:
            messages.info(req,"Password didn't match") 
            return redirect('signup')
        


    
    
    else:
        return render(req,"core/signup.html")
    
def signin(req):
    if req.method=="POST":
        username=req.POST['username']
        password=req.POST['password']

        user=auth.authenticate(username=username,password=password)
        if user is not None:
            auth.login(req,user)
            return redirect('index')
        
        else:
            messages.info(req,'Credentials Invalid!')
            return redirect('signin')
        
    
    else:
        return render(req,"core/signin.html")
    

@login_required(login_url='signin')
def logout(req):
    auth.logout(req)
    return redirect('signin')

@login_required(login_url='signin')
def settings(request):

    user_profile=Profile.objects.get(user=request.user) # fetches the current user
    if request.method=="POST":
        if request.FILES.get('image')==None:
            current_image=user_profile.profile_image
            bio=request.POST['bio']
            location=request.POST['location']

            user_profile.profile_image=current_image
            user_profile.bio=bio
            user_profile.location=location
            user_profile.save()

        if request.FILES.get('image')!=None:
            current_image=request.FILES.get('image')
            bio=request.POST['bio']
            location=request.POST['location']

            user_profile.profile_image=current_image
            user_profile.bio=bio
            user_profile.location=location
            user_profile.save()

        return redirect('settings')
    return render(request,'core/setting.html',{'user_profile':user_profile})



@login_required(login_url='signin')

def search(req):
    object_user=User.objects.get(username=req.user.username)
    user_profile = Profile.objects.filter(user=object_user)
    # code for other profiles containing subtring in their name
    if req.method=="POST":
        username=req.POST['username']
        profiles_id=User.objects.filter(username__icontains=username)
        profiles=[]
        for profile_id in profiles_id:
            profiles.append(Profile.objects.filter(user_id=profile_id.id))
        
        profiles=list(chain(*profiles))
       
    return render(req,"core/search.html",{'profiles':profiles,'user_profile':user_profile})



@login_required(login_url='sigin')
def profile(request,id):
    user_object=User.objects.get(username=id)
    user_profile=Profile.objects.get(user=user_object)
    user_posts=Post.objects.filter(user=id)
    user_posts_len=len(user_posts)
    follower=request.user.username
    user=id

    if FollowersCount.objects.filter(follower=follower,user=user).first():
        button_text="unfollow"
    else:
        button_text="follow"

    user_followers=len(FollowersCount.objects.filter(user=id))
    user_following=len(FollowersCount.objects.filter(follower=id))

    context={
        'user_object':user_object,
        'user_profile':user_profile,
        'user_posts_len':user_posts_len,
        'user_posts':user_posts,
        'button_text':button_text,
        'user_followers':user_followers,
        'user_following':user_following

    }

    return render(request,'core/profile.html',context)

@login_required(login_url='sigin')
def follow(request):
    if request.method=="POST":
        follower=request.POST['follower']
        user=request.POST['user']



        if FollowersCount.objects.filter(follower=follower,user=user).first():
            delete_follower=FollowersCount.objects.get(follower=follower,user=user)
            delete_follower.delete()
            return redirect('profile/'+user)
        else:
            new_follower=FollowersCount.objects.create(follower=follower,user=user)
            new_follower.save()
            return redirect('profile/'+user)



    else:
        return redirect("index")
    


def delete_(request,id):
    delete_post=Post.objects.get(id=id)
    user_post_name=delete_post.user
    current_user=request.user.username
    if request.method=="POST":
        
        if current_user!=user_post_name:
            return redirect('index')

        else:
            delete_post.delete()
            return redirect('index')
        
    
        
   
        
    
 
            
    