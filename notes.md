git add * (adds all)
git commit -m "first commit" (stores it as is)
then need to upload or push
git remote add origin https://github.com/APandoe/Project.git
git push -u origin master (tells you how to get it in)

<!--HOW TO EDIT TO MAKE HEROKU FRIENDLY-->
<!--add to Procfile-->
web: gunicorn application:app

<!--to refresh and add new files-->
git add Procfile
git commit -m "Add Procfile"
git push

<!--now heroku knows what to do new code-->
automatic deploys

<!--add database-->
postgres database

no longer have SQL("finance.db") change to link in Heroku (URI)

pgloader finance.db URI?ssslmode=require

adminer50 like PHPLite, might need update50

manual.cs50.net/heroku/

what about buying vpns?
so what does heroku do?
    does it just create the vps and dns?

https://github.com/APandoe/IdiotSandwich.git