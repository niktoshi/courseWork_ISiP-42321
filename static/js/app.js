// файл содержит клиентскую интерактивность сайта, которая выполняется в браузере
// обработчик клика на документе работает через делегирование событий для разных элементов страницы
document.addEventListener('click', function (e) {
  // ищем, был ли клик по миниатюре изображения товара
  const thumb = e.target.closest('.thumb-button');
  if (thumb) {
    // убираем активное состояние со всех миниатюр и ставим его на выбранную
    document.querySelectorAll('.thumb-button').forEach((btn) => btn.classList.remove('active'));
    thumb.classList.add('active');

    // меняем главное изображение товара на картинку из data-image у выбранной миниатюры
    const mainImage = document.getElementById('main-product-image');
    if (mainImage) mainImage.src = thumb.dataset.image;
  }

  // для кликабельных элементов добавляем короткую CSS-анимацию нажатия
  const pulseTarget = e.target.closest('.solid-btn, .ghost-btn, .soft-btn, .icon-btn, .cart-pill, .filter-link, .tag-list a, .main-nav a');
  if (pulseTarget) {
    // сначала снимаем класс, чтобы повторный клик мог заново запустить анимацию
    pulseTarget.classList.remove('tap-pop');
    window.requestAnimationFrame(() => pulseTarget.classList.add('tap-pop'));
  }
});

// IntersectionObserver отслеживает появление карточек/блоков в зоне видимости экрана
const observer = new IntersectionObserver((entries) => {
  entries.forEach((entry) => {
    if (entry.isIntersecting) {
      // когда элемент появился на экране, добавляем класс revealed для плавного появления
      entry.target.classList.add('revealed');
      //  после первого появления перестаём следить за элементом, чтобы не делать лишнюю работу
      observer.unobserve(entry.target);
    }
  });
}, { threshold: 0.12 });

// выбираем основные блоки, которые должны плавно появляться при прокрутке страницы
document.querySelectorAll('.section-block, .product-card, .service-card, .category-tile, .inspiration-card, .reveal-item').forEach((el) => {
  // передаём каждый найденный элемент наблюдателю
  observer.observe(el);
});
