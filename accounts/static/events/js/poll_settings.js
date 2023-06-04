document.addEventListener('click', function (e) {
    console.log(e.target.id)
    if (e.target.id != 'options') {
        var optionsdiv = document.getElementById('options-div')
        optionsdiv.classList.add('d-none')
    }
})

var editTitle = document.getElementById('editTitle')
var editDetails = document.getElementById('editDetails')
var editLocation = document.getElementById('editLocation')
var editRsvp = document.getElementById('editRsvp')
var addDate = document.getElementById('addDate')
var removeDate = document.getElementById('removeDate')
var closePoll = document.getElementById('closePoll')
var openPoll = document.getElementById('openPoll')
var deletePoll = document.getElementById('deletePoll')
var changeName = document.getElementById('changeName')
var closebtn = document.getElementById('closeModal')
var submitbtn = document.getElementById('changes')

var now = new Date();

// Set the minimum date and time for the input
var year = now.getFullYear();
var month = now.getMonth() + 1;
var day = now.getDate();
var hours = now.getHours();
var minutes = now.getMinutes();
var minDate = year + '-' + addLeadingZero(month) + '-' + addLeadingZero(day) + 'T' + addLeadingZero(hours) + ':' + addLeadingZero(minutes);

function addLeadingZero(number) {
    if (number < 10) {
        return '0' + number;
    }
    return number;
}

var optionsbtn = document.getElementById('options')
optionsbtn.addEventListener('click', () => {
    var optionsdiv = document.getElementById('options-div')
    if (optionsdiv.classList.contains('d-none'))
        optionsdiv.classList.remove('d-none')
    else
        optionsdiv.classList.add('d-none')
})

if (editTitle) {
    editTitle.addEventListener('click', () => {
        openModal()
        editModalLabel('Edit Name')
        appendToModal('input', 'text', 'event_name', 'Name', event_name)
        submitbtn.innerText = 'Save'
    })
}

if (editDetails) {
    editDetails.addEventListener('click', () => {
        openModal()
        editModalLabel('Edit Details')
        appendToModal('textarea', 'text', 'event_details', 'Details', event_details)
        submitbtn.innerText = 'Save'
    })
}

if (addDate) {
    addDate.addEventListener('click', () => {
        openModal()
        editModalLabel('Add Date/Time')
        appendToModal('input-input', ['date', 'time'], ['date', 'start', 'end'], ['Date', 'Start', 'End'], '')
        submitbtn.innerText = 'Add'
    })
}

if (removeDate) {
    removeDate.addEventListener('click', () => {
        openModal()
        editModalLabel('Remove Date/Time')
        //document.getElementById('edit-form').action = ""
        console.log(JSON.parse(slots)[0])
        var div = createDiv('mb-3')
        JSON.parse(slots).forEach(slot => {
            var input = createInput('checkbox', 'timeslots[]', slot.pk, '')
            var options = { weekday: 'short', month: 'short', day: 'numeric' };
            var datef = new Date(slot.fields.day);
            datef = datef.toLocaleDateString("en-US", options)
            var p = createLabel(datef + ' @ ' + slot.fields.start + ' - ' + slot.fields.end, 'form-label ml-3')
            div.append(input)
            div.append(p)
            div.append(document.createElement('br'))
        });

        var content = document.getElementById('modalContent')
        if (content.children.length > 2) {
            content.removeChild(content.children[2])
        }
        content.append(div)
        submitbtn.innerText = 'Remove Selected'
    })
}

if (editLocation) {
    editLocation.addEventListener('click', () => {
        openModal()
        editModalLabel('Edit Location')
        appendToModal('input', 'text', 'event_location', 'Location', event_location)
        submitbtn.innerText = 'Save'
    })
}

if (editRsvp) {
    editRsvp.addEventListener('click', () => {
        openModal()
        editModalLabel('Edit RSVP')
        appendToModal('input', 'datetime-local', 'rsvp_by', 'RSVP', event_rsvp)
        submitbtn.innerText = 'Save'
    })
}

if (changeName) {
    changeName.addEventListener('click', () => {
        openModal()
        editModalLabel('Change Your Name')
        appendToModal('input', 'text', 'name', 'Name', guest.fields.name)
        submitbtn.innerText = 'Save'
        var form = document.getElementById('edit-form')
        form.action = "/guests/" + guest.fields.custom_id + '/edit'
    })
}

if (closePoll) {
    closePoll.addEventListener('click', () => {
        openModal()
        editModalLabel('Close Poll')
        appendToModal('p-input', 'checkbox', 'notify', 'Notify your guests via email', 'You are about to close your poll')
        submitbtn.innerText = 'Close'
    })
}

if (openPoll) {
    openPoll.addEventListener('click', () => {
        openModal()
        editModalLabel('Remove Date/Time')
        //document.getElementById('edit-form').action = ""
        var content = document.getElementById('modalContent')
        content.innerHTML = content.innerHTML + '<div class="mb-2"><p class="text-center">You are about to re-open a poll which you already closed. If you have already picked/selected a date/time for your event it will be un-selected.</p>'
            + '<label class="form-label">RSVP by</label>'
            + '<input type="datetime-local" class="form-control" name="rsvp_by" id="re_open"><br>'
            + '<input type="checkbox" name="notify">'
            + '<label type="form-label ml-3"> Notify guests with email</label></div>'
        document.getElementById('re_open').setAttribute('min', minDate)
        submitbtn.innerText = 'Save'
    })
}

if (deletePoll) {
    deletePoll.addEventListener('click', () => {
        openModal()
        editModalLabel('Delete Poll')
        appendToModal('p-p', '', '', '', ['Are you sure you want to permanently DELETE your poll?', 'Your poll cannot be reinstated if deleted.'])
        submitbtn.innerText = 'Delete'
    })
}
if (closebtn) {
    closebtn.addEventListener('click', () => {
        const modal = document.getElementById('editModal')
        modal.style.display = 'none';
    });
}

function openModal() {
    const modal = document.getElementById('editModal')
    modal.style.display = 'block'
}

function editModalLabel(label) {
    var modalLabel = document.getElementById('editModalLabel')
    modalLabel.innerText = label
}

function createDiv(attr) {
    var inputdiv = document.createElement('div')
    inputdiv.setAttribute('class', attr)

    return inputdiv
}

function createLabel(label, attr) {
    var inputLabel = document.createElement('label')
    inputLabel.setAttribute('class', attr)
    inputLabel.innerText = label

    return inputLabel
}

function createInput(type, name, value, attr) {
    var inputField = document.createElement('input')
    inputField.setAttribute('type', type)
    inputField.setAttribute('class', attr)
    inputField.setAttribute('name', name)
    inputField.setAttribute('value', value)
    if (name == 'rsvp_by') {
        inputField.setAttribute('min', minDate)
    }

    return inputField
}

function createTextArea(type, name, value) {
    var inputField = document.createElement('textarea')
    inputField.setAttribute('class', 'form-control')
    inputField.setAttribute('name', name)
    inputField.setAttribute('rows', 5)
    inputField.innerText = value

    return inputField
}

function createParagraph(value) {
    var message = document.createElement('p')
    message.setAttribute('class', 'text-center')
    message.innerText = value

    return message;
}

function appendToModal(input, type, name, label, value) {
    var inputdiv = createDiv()
    var form = document.getElementById('edit-form')
    //form.action = ""
    if (input == 'p-p') {
        form.action = delete_url
        form.children[0].children[1].value = 'delete'
        p1 = createParagraph(value[0])
        p2 = createParagraph(value[1])

        inputdiv.append(p1)
        inputdiv.append(p2)
    } else {
        if (input == 'p-input') {
            p = createParagraph(value)
            hiddenInput = createInput('hidden', 'close', '', '')
            inputField = createInput(type, name, '', '')
            inputLabel = createLabel(label, 'form-label ml-3')
            inputdiv.append(p)
            inputdiv.append(hiddenInput)
            inputdiv.append(inputField)
            inputdiv.append(inputLabel)
        } else if (input == 'input') {
            inputLabel = createLabel(label, 'form-label')
            inputField = createInput(type, name, value, 'form-control')
            inputdiv.append(inputLabel)
            inputdiv.append(inputField)
        } else if (input == 'textarea') {
            inputLabel = createLabel(label, 'form-label')
            inputField = createTextArea(type, name, value, 'form-control')
            inputdiv.append(inputLabel)
            inputdiv.append(inputField)
        } else if (input == 'input-input') {
            inputdiv = createDiv('mb-3 row justify-content-between')
            datediv = createDiv('col-md-4')
            startdiv = createDiv('col-md-4')
            enddiv = createDiv('col-md-4')

            dateLabel = createLabel(label[0], 'form-label')
            startLabel = createLabel(label[1], 'form-label')
            endLabel = createLabel(label[2], 'form-label')

            dateField = createInput(type[0], name[0], value)
            startField = createInput(type[1], name[1], value, 'form-control')
            endField = createInput(type[1], name[2], value, 'form-control')

            dateField.setAttribute('required', 'required')
            var minDay = year + '-' + addLeadingZero(month) + '-' + addLeadingZero(day);
            dateField.setAttribute('min', minDay)
            startField.setAttribute('required', 'required')
            endField.setAttribute('required', 'required')

            datediv.append(dateLabel)
            datediv.append(dateField)

            startdiv.append(startLabel)
            startdiv.append(startField)

            enddiv.append(endLabel)
            enddiv.append(endField)

            inputdiv.append(datediv)
            inputdiv.append(startdiv)
            inputdiv.append(enddiv)
        }

    }
    var form = document.getElementById('modalContent')
    if (form.children.length > 2) {
        form.removeChild(form.children[2])
    }
    form.append(inputdiv)
}