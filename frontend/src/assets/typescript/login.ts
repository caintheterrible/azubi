// Waiting for DOM to load

document.addEventListener('DOMContentLoaded', ()=>{
    const loginForm=document.getElementById('loginForm') as HTMLFormElement | null;

    if (!loginForm) return;

    loginForm.addEventListener('submit', async(event:Event)=>{
        event.preventDefault();

        // Get login form data
        const formData=new FormData(loginForm);
        const data={
            email:formData.get('email') as string,
            password:formData.get('password') as string,
        };

        try{
            const response:Response=await fetch('http://localhost:8000/auth/login/', {
                method:'POST',
                headers:{
                    'Content-Type':'application/json',
                },
                body:JSON.stringify(data),
            });

            const result=await response.json();

            if (response.ok){
                alert(result.message || 'Login successful!');
                loginForm.reset();
                window.location.href='../pages/dashboard.html';
            } else{
                alert(result.error || 'Login failed. Please try again later.')
            }

        } catch (err){
            alert(`An error occurred: ${err}`);
        }
    });
});