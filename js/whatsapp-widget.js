(function () {
  'use strict';

  var phoneNumber = '12316203620';
  var message =
    "Hey! Bret Schrader, I have visited your website and I'm interested in getting your services. Can we connect?";
  var whatsappUrl = 'https://wa.me/' + phoneNumber + '?text=' + encodeURIComponent(message);

  function createWidget() {
    var container = document.createElement('div');
    container.id = 'whatsapp-widget';
    container.style.cssText =
      'position:fixed;bottom:90px;right:20px;z-index:9999;display:flex;align-items:center;gap:12px;font-family:Montserrat,sans-serif;direction:rtl;';

    var tooltip = document.createElement('span');
    tooltip.id = 'whatsapp-tooltip';
    tooltip.textContent = 'Chat with us';
    tooltip.style.cssText =
      'background:#071d49;color:#fff;padding:10px 18px;border-radius:20px;font-size:13px;font-weight:500;opacity:0;transform:translateX(10px);transition:all 0.3s ease;pointer-events:none;white-space:nowrap;box-shadow:0 2px 12px rgba(0,0,0,0.15);';

    var btn = document.createElement('a');
    btn.href = whatsappUrl;
    btn.target = '_blank';
    btn.rel = 'noopener noreferrer';
    btn.id = 'whatsapp-btn';
    btn.setAttribute('aria-label', 'Chat with us on WhatsApp');
    btn.style.cssText =
      'display:flex;align-items:center;justify-content:center;width:56px;height:56px;border-radius:50%;background:#25D366;box-shadow:0 4px 16px rgba(37,211,102,0.45);transition:all 0.3s ease;cursor:pointer;text-decoration:none;flex-shrink:0;animation:whatsappPulse 2s ease-in-out infinite;';

    btn.innerHTML =
      '<svg viewBox="0 0 24 24" width="28" height="28" fill="white" xmlns="http://www.w3.org/2000/svg"><path d="M17.472 14.382c-.297-.149-1.758-.867-2.03-.967-.273-.099-.471-.148-.67.15-.197.297-.767.966-.94 1.164-.173.199-.347.223-.644.075-.297-.15-1.255-.463-2.39-1.475-.883-.788-1.48-1.761-1.653-2.059-.173-.297-.018-.458.13-.606.134-.133.298-.347.446-.52.149-.174.198-.298.298-.497.099-.198.05-.371-.025-.52-.075-.149-.669-1.612-.916-2.207-.242-.579-.487-.5-.669-.51-.173-.008-.371-.01-.57-.01-.198 0-.52.074-.792.372-.272.297-1.04 1.016-1.04 2.479 0 1.462 1.065 2.875 1.213 3.074.149.198 2.096 3.2 5.077 4.487.709.306 1.262.489 1.694.625.712.227 1.36.195 1.871.118.571-.085 1.758-.719 2.006-1.413.248-.694.248-1.289.173-1.413-.074-.124-.272-.198-.57-.347m-5.421 7.403h-.004a9.87 9.87 0 01-5.031-1.378l-.361-.214-3.741.982.998-3.648-.235-.374a9.86 9.86 0 01-1.51-5.26c.001-5.45 4.436-9.884 9.888-9.884 2.64 0 5.122 1.03 6.988 2.898a9.825 9.825 0 012.893 6.994c-.003 5.45-4.437 9.884-9.885 9.884m8.413-18.297A11.815 11.815 0 0012.05 0C5.495 0 .16 5.335.157 11.892c0 2.096.547 4.142 1.588 5.945L.057 24l6.305-1.654a11.882 11.882 0 005.683 1.448h.005c6.554 0 11.89-5.335 11.893-11.893a11.821 11.821 0 00-3.48-8.413z"/></svg>';

    container.appendChild(btn);
    container.appendChild(tooltip);

    document.body.appendChild(container);

    var tooltipTimer = setTimeout(function () {
      tooltip.style.opacity = '1';
      tooltip.style.transform = 'translateX(0)';
    }, 1500);

    setTimeout(function () {
      tooltip.style.opacity = '0';
      tooltip.style.transform = 'translateX(10px)';
    }, 5500);

    container.addEventListener('mouseenter', function () {
      clearTimeout(tooltipTimer);
      tooltip.style.opacity = '1';
      tooltip.style.transform = 'translateX(0)';
    });

    container.addEventListener('mouseleave', function () {
      tooltip.style.opacity = '0';
      tooltip.style.transform = 'translateX(10px)';
    });

    btn.addEventListener('mouseenter', function () {
      btn.style.transform = 'scale(1.08)';
      btn.style.boxShadow = '0 6px 20px rgba(37,211,102,0.6)';
    });

    btn.addEventListener('mouseleave', function () {
      btn.style.transform = 'scale(1)';
      btn.style.boxShadow = '0 4px 16px rgba(37,211,102,0.45)';
    });

    var style = document.createElement('style');
    style.textContent =
      '\n      @keyframes whatsappPulse {\n        0% { box-shadow: 0 4px 16px rgba(37,211,102,0.45); }\n        50% { box-shadow: 0 4px 28px rgba(37,211,102,0.75); }\n        100% { box-shadow: 0 4px 16px rgba(37,211,102,0.45); }\n      }\n      @media (max-width: 768px) {\n        #whatsapp-widget { bottom: 70px !important; right: 14px !important; }\n        #whatsapp-btn { width: 48px !important; height: 48px !important; }\n        #whatsapp-btn svg { width: 24px !important; height: 24px !important; }\n      }\n    ';
    document.head.appendChild(style);
  }

  if (document.readyState === 'loading') {
    document.addEventListener('DOMContentLoaded', createWidget);
  } else {
    createWidget();
  }
})();
