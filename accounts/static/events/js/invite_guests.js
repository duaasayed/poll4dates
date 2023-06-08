var invite_guest = document.getElementById('invite-guest')
var guests = document.getElementById('guests')
if (invite_guest) {
    invite_guest.addEventListener('keypress', (event) => {
        if (event.key == 'Enter' || event.key == ',') {
            event.preventDefault()
            let i = guests.children.length
            guests.innerHTML = guests.innerHTML + '<p onclick="hide(this)" style="cursor:pointer" id="guest-' + i + 1 + '">' + invite_guest.value + '</p>'
            invite_guest.value = ''
        }
    })
}


var send_invite = document.getElementById('send-invite')
var guest_list = document.getElementById('guest-list')

if (send_invite) {
    send_invite.addEventListener('click', (e) => {
        e.preventDefault()
        invites = guests.children
        var form = document.getElementById('addGuestForm')

        for (let i = 0; i < invites.length; i++) {
            form.innerHTML = form.innerHTML + '<input type="hidden" name="guest_list[]" value="' + invites[i].innerText + '">'
        }

        form.submit()

    })
}

function hide(element) {
    n = element.id.split('-')[1]
    element.parentElement.removeChild(element)
}