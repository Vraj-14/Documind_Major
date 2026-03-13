// const API_URL = "http://127.0.0.1:8000/ask";
const API_URL = "http://localhost:8000/ask";


async function askBackend(question){

const response = await fetch(API_URL,{

method:"POST",

headers:{
"Content-Type":"application/json"
},

body:JSON.stringify({
question:question
})

});

return await response.json();

}