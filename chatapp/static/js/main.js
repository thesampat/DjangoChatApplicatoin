var ws = new WebSocket('ws://127.0.0.1:8000/chat/')
var user_status = 'offline'
var messagebadge = 1
listbuttons = document.getElementsByClassName('listbuttons')
chatDisplayName = document.querySelector('#chatDisplayName')
listUser = document.querySelector('#listuser')
chatScreen = document.querySelector('#chatScreen')
let target_user = 'None'
let requestUser = document.querySelector('#requestUser').innerHTML;
let chatWindow = document.querySelector('#chatWindow')
let statusDisplay = document.getElementById('statusOnline')
let isgroup = 0
let group = 'None'


function select(event){
chatDisplayName.innerText = event
target_user = event
chatScreen.innerHTML  = ''
chatWindow.style.visibility = 'visible'
isgroup = 0;

if (requestUser != target_user){
let badge = document.querySelector(`#badge_${target_user}`)
badge.style.display = 'none'
badge.innerHTML = '';

if (target_user.match('_') != null){
    let strcheck = target_user.split('_')
    isgroup = strcheck.indexOf('Group')

    if (group == 'None'){
        if (isgroup == 1){
            chatScreen.innerHTML += `<div class="btn-lg btn-block btn-light text-center" id='${target_user}' onClick='joinGroup(event)'>Join Group Now</div>`
        }
    }

}

}

let typechat = 'private'

if (isgroup == 1){
    typechat = 'group'
}

axios.get(`http://127.0.0.1:8000/status/${target_user}/`).then(
    function(res){
        
    if(isgroup == 1){
        statusDisplay.innerHTML = '200 Members'
    }
    else{
        if (typeof(res['data']) == 'string'){
            statusDisplay.innerHTML = res['data']
        }   
        else{
            statusDisplay.innerHTML = 'online'
        }  
    }
}
)

axios.get(`http://127.0.0.1:8000/chats/${requestUser}/${target_user}/${typechat}/`)
.then(function(res){
let json_data = JSON.parse(res['data'])
console.log(json_data)
let fpr;
let spr;

for(data of json_data['chats']){
    if (isgroup == 1){
        fpr = (data['receipt']).split('-')[0]
        spr = (data['receipt']).split('-')[1]
    }
    else{
        fpr = (data['receipt']).split('_')[0]
        spr = (data['receipt']).split('_')[1]
    }
    
    let chat_data = {
    'message': data['chat'],
        'to_user':fpr,
        'from_user' : spr,
        'time': data['time'],
        'lastseen' : json_data['last_seen']
    }

    if (data['chat'] != ''){
        createBubbles(chat_data)
    }

}
})
}

function joinGroup(e){
    let data = {
        'type': 'group_join',
        'message': textData.value,
        'to_user':target_user,
        'from_user' : requestUser,
        }

    group = target_user
    ws.send(JSON.stringify(data))
    e.target.style.display='None'
}


textData = document.querySelector('#textData')

function sendMessage(e){

    let data = ''
    if (isgroup == 1){
        data = {
            'type': 'group_send',
            'message': textData.value,
            'to_user':target_user,
            'from_user' : requestUser,
            }
    }
    else{

        data = {
            'type': 'private',
            'message': textData.value,
            'to_user':target_user,
            'from_user' : requestUser,
            }
        
    }

    textData.value = ''
    ws.send(JSON.stringify(data))
} 

ws.onmessage = function(event){
type = JSON.parse(event.data)['typeof']
data = JSON.parse(event.data)['message']
time = JSON.parse(event.data)['time']


if (isgroup == 1){
    statusDisplay.innerHTML = '200 Members'
} 

else{
    if (type == 'system'){
        if (time == 'online'){
            statusDisplay.innerHTML = 'online'
        }   
        else{
            statusDisplay.innerHTML = time
        }
    }   
}

  

if(type == 'private' || type=='group_send'){

if (type == 'group_send'){
    if (requestUser !== data['from_user']){
        let badge
        badge = document.querySelector(`#badge_${data["to_user"]}`) 

        badge.style.display = '';
        badge.innerHTML = Number(badge.innerHTML) + messagebadge
    }
}

else{
    if (target_user != data['from_user']){
        let badge;
    
        if (requestUser != data['from_user']){
        badge = document.querySelector(`#badge_${data["from_user"]}`)
    
        badge.style.display = '';
        badge.innerHTML = Number(badge.innerHTML) + messagebadge
        }
    } 
}
    
    
    let chat_data = {
        'message': data['message'],
        'to_user':data['to_user'],
        'from_user' : data['from_user'],
        'time': time
    }


    if (isgroup ==1){
        if(chatDisplayName.innerText == data['to_user'])
    { if (target_user != 'None' ){
        createBubbles(chat_data)
        }
    }
    }

    else{
        if(chatDisplayName.innerText == data['to_user'] || chatDisplayName.innerText == data['from_user'])
        { if (target_user != 'None' ){
            createBubbles(chat_data)
            }
        }
    }
   
}



}

function createBubbles(data){

let time2 = new Date(data['time'])
hours = time2.getHours()
minutes = time2.getMinutes()
minutes = (minutes<10)? `0${minutes}`: `${minutes}`;


suffix = (hours >= 12)? 'pm' : 'am';
hours = (hours >= 12)? hours-12: hours;
time = `${hours}:${minutes} ${suffix}`

if (requestUser == data['from_user']){
chatScreen.innerHTML +=  
`<li class="d-flex mb-4"> 
<img src="https://mdbcdn.b-cdn.net/img/Photos/Avatars/avatar-6.webp" alt="avatar"
    class="rounded-circle d-flex align-self-start me-3 shadow-1-strong" width="60">
<div class="card">
    <div class="card-header d-flex justify-content-between p-3">
    <p class="fw-bold mb-0">${requestUser}</p>
    <p class="text-muted small mb-0">
        <i class="far fa-clock"></i>
        ${time}
    </p>
    </div>
    <div class="card-body">
    <p class="mb-0">
        ${data['message']}
    </p>
    </div>
</div>
</li>`
}

else{
chatScreen.innerHTML += `
<li class="d-flex justify-content-end mb-4">
    <div class="card">
    <div class="card-header d-flex justify-content-between p-3">
        <p class="fw-bold mb-0">${data['from_user']}</p>
        <p class="text-muted small mb-0"><i class="far fa-clock"></i>${time}</p>
    </div>
    <div class="card-body">
        <p class="mb-0">
        ${data['message']}
        </p>
    </div>
    </div>
    <img src="https://mdbcdn.b-cdn.net/img/Photos/Avatars/avatar-5.webp" alt="avatar"
    class="rounded-circle d-flex align-self-start ms-3 shadow-1-strong" width="60">
</li> `
}
}
