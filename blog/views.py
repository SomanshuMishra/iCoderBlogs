from django.shortcuts import render , HttpResponse ,redirect
from blog.models import Post , BlogComment
from django.contrib  import messages
from blog.templatetags import extras


# Create your views here.
def blogHome(request):
    allpPosts = Post.objects.all() 
    context = {'allPosts': allpPosts}
    return render(request,'blog/blogHome.html', context)

def blogPost(request , slug):
    post = Post.objects.filter(slugfields=slug)     
    comments = BlogComment.objects.filter(post__in=post, parent=None)
    # alls = BlogComment.objects.filter()
    # print("alls",alls)
    replies = BlogComment.objects.filter(post__in=post).exclude(parent=None)
    replyDict={}
    # print(comments,replies)
    for reply in replies:
        if reply.parent.sno not in replyDict.keys():
            replyDict[reply.parent.sno] = [reply]
        else:
            replyDict[reply.parent.sno].append(reply)
    print("ReplyDict",replyDict)
    context = {'post': post,'comments':comments,'replyDict':replyDict}
    return render(request,'blog/blogPost.html',context)


def postComment(request):
    if request.method=="POST":
        comment = request.POST.get("comment")       
        user = request.user
        postSno = request.POST.get("postSno")
        post = Post.objects.get(sno=postSno)
        parenSno = request.POST.get("parentSno")
        if comment =="":
            messages.error(request,'Comment Characters are very less')
            return redirect(f'/blog/{post.slugfields}')
        else:
            if parenSno=="":
                comment =BlogComment(comment=comment,user=user ,post=post)
                comment.save()
                messages.success(request,'Your Comment has been posted successfully')

            else:
                parent = BlogComment.objects.get(sno=parenSno)
                comment =BlogComment(comment=comment,user=user ,post=post,parent=parent)
                comment.save()
                messages.success(request,'Your Reply has been posted successfully')
        

    return redirect(f'/blog/{post.slugfields}')

def bloglogin(request):
    return HttpResponse('<h1 align="center">Please Go to Home Page to Login</h1>')
