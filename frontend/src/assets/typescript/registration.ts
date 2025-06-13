// Waiting for DOM to load

document.addEventListener('DOMContentLoaded', ()=> {
    const form= document.getElementById('registrationForm') as HTMLFormElement | null;

    if (!form) return;

    form.addEventListener('submit', async(event:Event)=>{
        event.preventDefault();

        // Get form data
        const formData=new FormData(form);
        const data={
            username:formData.get('username') as string,
            email:formData.get('email') as string,
            password:formData.get('password') as string,
        };

        try{
            const response=await fetch('http://localhost:8000/auth/register/', {
                method:'POST',
                headers:{
                    'Content-Type':'application/json',
                },
                body:JSON.stringify(data),
            });

            const result=await response.json();

            if (response.ok) {
                alert(result.message || 'User registered successfully!')
                form.reset();
                window.location.href = 'frontend/src/assets/pages/dashboard.html';
            } else {
                alert(result.error || 'Registration failed!');
            }

        } catch (error){
            alert('An error occurred: '+error);
        }
    });
});