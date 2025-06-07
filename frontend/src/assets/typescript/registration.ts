interface RegisterPayload{
    username:string;
    email:string;
    password:string;
}

interface RegisterResponse{
    message?:string;
    error?:string;
}

// CSRF token helper configuration
function getCSRFToken():string | null{
    const name='csrftoken';
    const cookies=document.cookie.split(';');

    for (const cookie in cookies){
        const trimmed=cookie.trim();
        if (trimmed.startsWith(name+'=')){
            return decodeURIComponent(trimmed.substring(name.length+1));
        }
    }

    return null;
}

async function submitRegistrationForm(event:Event):Promise<void>{
    event.preventDefault();

    const form=event.target as HTMLFormElement;
    const username=(form.querySelector('[name="username"]') as HTMLInputElement).value;
    const email=(form.querySelector('[name="email"]') as HTMLInputElement).value;
    const password=(form.querySelector('[name="password"]') as HTMLInputElement).value;

    const payload:RegisterPayload={
        username, email, password
    };

    try{
        // To later fetch from .env file instead
        const response=await fetch("http://localhost:8000/auth/register/", {
            method:'POST',
            headers:{
                'Content-Type':'application/json',
                // 'X-CSRFToken':getCSRFToken() || '' // activate when using CSRF protection
            },
            body:JSON.stringify(payload),
        });

        const data:RegisterResponse=await response.json();

        if (response.ok){
            alert(data.message || 'SUCCESS: Registration was successful!');
        } else{
            alert(data.error || 'ERROR: Registration failed');
        }

    } catch (error:any){
        alert('INTERNAL SERVER ERROR: An error occurred during registration attempt: '+error.message);
    }
}

// Event listener for when DOM is ready
document.addEventListener('DOMContentLoaded', ()=>{
    const form=document.getElementById('registrationForm') as HTMLFormElement || null;
    if (form){
        form.addEventListener('submit', submitRegistrationForm);
    } else{
        console.error('ERROR: Registration form not found in DOM!');
    }
})