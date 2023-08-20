function toggleModal() {
    let modal = document.querySelector('.modal')
    modal.classList.toggle('is-active')
}

function deleteItem(pk) {
    document.cookie = 'pk=' + pk
    toggleModal()
}

