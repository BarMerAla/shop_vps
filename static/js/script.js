$(document).ready(function () {
console.log('скрипт работает');
console.log("Сколько скрытых брендов найдено:", $('.hidden-brand').length);
const wrapper = document.getElementById('brand-wrapper');
const toggleLink = $('#toggle-brands');
const hiddenBrands = $('.hidden-brand');
let expanded = false;
const searchInput = document.getElementById('searchInput');
const searchForm = document.getElementById('searchForm');
let timeout = null;

if (hiddenBrands.length === 0) {
    toggleLink.hide();
    return;
}

hiddenBrands.show();

const hasCheckedHiddenBrands = hiddenBrands.find('input:checked').length > 0;
console.log("Отмеченные скрытые бренды:", hasCheckedHiddenBrands);

if (!hasCheckedHiddenBrands) {
    hiddenBrands.hide();
} else {
        expanded = true;
        toggleLink.text('Скрыть бренды');
    }


requestAnimationFrame(() => {
    const visibleItems = wrapper.querySelectorAll('.brand-item:not([style*="display: none"])');
    const visibleHeight = Array.from(visibleItems).reduce((acc, item) => acc + item.offsetHeight, 0);
    wrapper.style.height = visibleHeight + 'px';
    });


toggleLink.on('click', function (event) {
    event.preventDefault();
    if (!expanded) {
        hiddenBrands.show();

        requestAnimationFrame(() => {
        const fullHeight = wrapper.scrollHeight;
        wrapper.style.height = fullHeight + 'px';
    });
        $(this).text('Скрыть бренды');
    }
    else {
        const visibleItems = wrapper.querySelectorAll('.brand-item:not(.hidden-brand):not([style*="display: none"])');
        const collapsedHeight = Array.from(visibleItems).reduce((acc, item) => acc + item.offsetHeight, 0);
        wrapper.style.height = collapsedHeight + 'px';

        setTimeout(() => {
            hiddenBrands.hide();
        }, 300);

        $(this).text('Все бренды');
        }
    expanded = !expanded;
    });

    searchInput.addEventListener('input', function () {
        clearTimeout(timeout);
        timeout = setTimeout(() => {
            searchForm.submit();  
        }, 500);  
    });
});

