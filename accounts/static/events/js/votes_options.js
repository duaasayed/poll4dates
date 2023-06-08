var votesbtn = document.getElementById('votes-op')
var calendarbtn = document.getElementById('calendar-op')
var tablebtn = document.getElementById('table-op')

votesbtn.addEventListener('click', () => {
    document.getElementById('calendar').classList.add('d-none')
    document.getElementById('table-body').classList.add('d-none')
    document.getElementById('votes-body').classList.remove('d-none')
})

calendarbtn.addEventListener('click', () => {
    var calendarEl = document.getElementById('calendar');
    calendarEl.classList.remove('d-none')
    var calendar = new FullCalendar.Calendar(calendarEl, {
        initialView: 'dayGridMonth',
        selectable: true,
        selectMirror: true,
        validRange: {
            start: Date.now(),
        },
        editable: true,
        eventDidMount: (cell) => {
            console.log(cell.event)
            var checkbox = document.createElement('input')
            checkbox.type = 'checkbox'
            checkbox.setAttribute('id', 'date-' + calendar.getDate())
            checkbox.setAttribute('style', 'transform: scale(1.5);accent-color:green')
            cell.el.children[0].children[0].append(checkbox)
            checkbox.value = cell.event.id
            console.log(guest)
            if (guest && guest.fields.choices) {
                guest.fields.choices.forEach(choice => {
                    if ((choice == cell.event.id)) {
                        checkbox.checked = true
                    }
                })
                checkbox.addEventListener('change', () => {
                    timeslot = checkbox.value
                    axios.defaults.xsrfHeaderName = "X-CSRFToken"
                    axios.defaults.xsrfCookieName = 'csrftoken'

                    let data = new FormData();

                    data.append("_method", 'put')
                    data.append("action", guest.fields.choices.includes(parseInt(timeslot)) ? 'remove' : 'add')
                    data.append("csrfmiddlewaretoken", '{{csrf_token}}')
                    data.append('timeslot', timeslot)

                    axios.post('http://127.0.0.1:8000/invites/{{event.poll_id}}/poll/' + guest.fields.custom_id, data)
                        .then(data => location.reload())
                })
            }
        }

    })
    calendar.render()
    var timeslots = JSON.parse('{{timeslots|queryset_as_json}}')
    console.log(timeslots)
    timeslots.forEach(timeslot => {
        var event = {
            'id': timeslot.pk,
            'title': timeslot.fields.start_time.split(':', 2).join(':'),
            'start': timeslot.fields.date
        }
        console.log(event)
        calendar.addEvent(event)
    });
    document.getElementById('table-body').classList.add('d-none')
    document.getElementById('votes-body').classList.add('d-none')
})

tablebtn.addEventListener('click', () => {
    document.getElementById('calendar').classList.add('d-none')
    document.getElementById('table-body').classList.remove('d-none')
    document.getElementById('votes-body').classList.add('d-none')
})