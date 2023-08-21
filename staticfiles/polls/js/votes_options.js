var votesbtn = document.getElementById('votes-op')
var calendarbtn = document.getElementById('calendar-op')
var tablebtn = document.getElementById('table-op')

votesbtn.addEventListener('click', () => {
    if (calendarbtn) {
        document.getElementById('calendar').classList.add('d-none')
    }
    if (tablebtn) {
        document.getElementById('table-body').classList.add('d-none')
    }
    document.getElementById('votes-body').classList.remove('d-none')
})


if (calendarbtn) {
    calendarbtn.addEventListener('click', () => {
        var calendarEl = document.getElementById('calendar');
        if (tablebtn) {
            document.getElementById('table-body').classList.add('d-none')
        }
        document.getElementById('votes-body').classList.add('d-none')
        calendarEl.classList.remove('d-none')
        var calendar = new FullCalendar.Calendar(calendarEl, {
            initialView: 'dayGridMonth',
            selectable: true,
            selectMirror: true,

            editable: true,
            eventDidMount: (cell) => {
                var checkbox = document.createElement('input')
                checkbox.type = 'checkbox'
                checkbox.setAttribute('id', 'date-' + cell.event.id)
                checkbox.setAttribute('style', 'transform: scale(1.5);accent-color:green')
                cell.el.children[0].children[0].append(checkbox)
                checkbox.value = cell.event.id
                var choice = document.getElementById(`choice-${cell.event.id}`)
                if (votes) {
                    votes.forEach(vote => {
                        if ((parseInt(vote.fields.time_slot) == cell.event.id)) {
                            checkbox.checked = true
                        }

                        checkbox.checked = choice.checked
                    })
                    checkbox.addEventListener('change', () => {
                        var timeslot = checkbox.value

                        if (guest == null) {
                            guestModal.style.display = 'block';
                        }


                        voteSocket.send(JSON.stringify({
                            'timeslot_id': parseInt(timeslot),
                            'guest_id': guest_id,
                            'vote_method': 'calendar'
                        }));

                    })
                }
            }

        })
        calendar.render()
        var timeslots = JSON.parse(slots)
        timeslots.forEach(timeslot => {
            var event = {
                'id': timeslot.pk,
                'title': timeslot.fields.start.split(':', 2).join(':'),
                'start': timeslot.fields.day
            }
            calendar.addEvent(event)

        });
    })
}


if (tablebtn) {
    tablebtn.addEventListener('click', () => {
        if (calendarbtn) {
            document.getElementById('calendar').classList.add('d-none')
        }
        document.getElementById('table-body').classList.remove('d-none')
        document.getElementById('votes-body').classList.add('d-none')
    })
}


