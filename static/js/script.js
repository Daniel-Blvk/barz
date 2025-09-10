'use strict';

const elemToggleFunc = function (elem) { elem.classList.toggle('active'); }

const navbar = document.querySelector('[data-navbar]');
const overlay = document.querySelector('[data-overlay]');
const navToggleBtn = document.querySelector('[data-nav-toggle-btn]');

const navElemArr = [overlay, navToggleBtn];

for(let i = 0; i < navElemArr.length; i++) {
    navElemArr[i].addEventListener('click', function () {
        elemToggleFunc(navbar);
        elemToggleFunc(overlay);
    });
}

// Header sticky

const headerElem = document.querySelector('[data-header]');
let lastScrollPosition = 0;

window.addEventListener('scroll', function () {
    let scrollPosition = window.pageYOffset;

    if(scrollPosition > lastScrollPosition) { 
        headerElem.classList.remove('active'); 
    } else { 
        headerElem.classList.add('active'); 
    }

    lastScrollPosition = scrollPosition <= 0 ? 0 : scrollPosition;
});

// Form validation

const input = document.querySelector('[data-input]');
const submitBtn = document.querySelector('[data-submit]');

if (input && submitBtn) {
    input.addEventListener('input', function () {
        if(input.checkValidity()) { 
            submitBtn.removeAttribute('disabled'); 
        } else { 
            submitBtn.setAttribute('disabled', ''); 
        }
    });
}

// Go top

const goTopBtn = document.querySelector('[data-go-top]');

if (goTopBtn) {
    window.addEventListener('scroll', function () {
        window.scrollY > 200 ? goTopBtn.classList.add('active') : goTopBtn.classList.remove('active');
    });
}

// Contact form handling
const contactForm = document.querySelector('.contact-form form');
if (contactForm) {
    contactForm.addEventListener('submit', function(e) {
        e.preventDefault();
        alert('Thank you for your message! We will get back to you soon.');
        contactForm.reset();
    });
}

// Newsletter form handling
const newsletterForm = document.querySelector('.card-form');
if (newsletterForm) {
    newsletterForm.addEventListener('submit', function(e) {
        e.preventDefault();
        alert('Thank you for subscribing to our newsletter!');
        newsletterForm.reset();
    });
}