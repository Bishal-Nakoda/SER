const spotlightSize = 400;

document.addEventListener('mousemove', function(event) {
    if (window.event) { // IE fix
        event = window.event;
    }
    // Get the coordinates of the title
    let titleRect = document.querySelector('.title').getBoundingClientRect();

    // Grab the mouse's X-position
    let mouseX = event.clientX;

    // Position spotlight x coordinate based on mouse x, center based on width of spotlight, take into account element x offset
    let spotlightX = mouseX - (spotlightSize / 2) - titleRect.left;

    // Grab the mouse's Y position
    let mouseY = event.clientY;

    // Position spotlight y coordinate based on mouse y, center based on width of spotlight, take into account element y offset
    let spotlightY = mouseY - (spotlightSize / 2) - titleRect.top;

    // Set x and y position of spotlight
    const element = document.querySelector('.title');
    element.style.backgroundPosition = spotlightX + 'px ' + spotlightY + 'px';
}, false);