(() => {
  'use strict';
  const plans = {
    assinatura: { name: 'Nelis Básico', price: 97, posts: 0, features: ['Conversa direta com a Nelis no Telegram', 'Ideias e sugestões de conteúdo', 'Criação de legendas', 'Planejamento de publicações', 'Criação de prompts para imagens', 'Não inclui arte pronta'] },
    essencial: { name: 'Essencial', price: 197, posts: 4, features: ['Acesso à Nelis incluído', '4 posts com arte pronta e legenda', '1 rodada de ajustes por post', 'Sugestões de temas ao longo do mês'] },
    assistida: { name: 'Assistida', price: 397, posts: 8, features: ['Acesso à Nelis incluído', '8 posts com arte pronta e legenda', '1 rodada de ajustes por post', 'Sugestões de temas ao longo do mês'] },
    presenca: { name: 'Presença', price: 597, posts: 12, features: ['Acesso à Nelis incluído', '12 posts com arte pronta e legenda', '1 rodada de ajustes por post', 'Prioridade de ajuste'] }
  };
  const money = value => new Intl.NumberFormat('pt-BR', { style: 'currency', currency: 'BRL' }).format(value);
  const el = id => document.getElementById(id);
  const hasPlan = key => Object.prototype.hasOwnProperty.call(plans, key);
  function paymentFor(key) {
    const settings = window.NELIS_PAYMENTS?.[key];
    if (!settings?.enabled || !['recurring', 'one_time'].includes(settings.mode)) return null;
    try {
      const url = new URL(settings.url);
      if (url.protocol !== 'https:' || url.username || url.password) return null;
      return { ...settings, url: url.href };
    } catch { return null; }
  }
  function showPlan(key, updateUrl = false) {
    const valid = hasPlan(key);
    document.querySelectorAll('input[name="plano"]').forEach(radio => { radio.checked = valid && radio.value === key; });
    el('empty-state').hidden = valid;
    el('order-details').hidden = !valid;
    el('included').hidden = !valid;
    el('payment-link').hidden = true;
    el('payment-link').removeAttribute('href');
    if (!valid) { document.title = 'Escolha seu plano — Nelis'; return; }
    const plan = plans[key];
    document.title = `Plano ${plan.name} — Nelis`;
    el('plan-name').textContent = plan.name;
    el('post-count').textContent = plan.posts ? `${plan.posts} posts` : 'Sem posts';
    el('price').textContent = money(plan.price);
    el('minimum-total').textContent = money(plan.price) + ' / mês';
    el('included-title').textContent = plan.posts
      ? `${plan.posts} posts, com a sua identidade.`
      : 'Nelis Básico: a assistente no seu Telegram.';
    el('features').replaceChildren(...plan.features.map(text => { const li = document.createElement('li'); li.textContent = text; return li; }));
    el('contact-link').href = `https://wa.me/5522996119580?text=${encodeURIComponent(`Olá! Quero contratar o plano ${plan.name} da Nelis, ${plan.posts ? `com ${plan.posts} posts por ${money(plan.price)} por mês` : `por ${money(plan.price)} por mês`}. Gostaria de confirmar as condições e a forma de pagamento.`)}`;
    const payment = paymentFor(key);
    if (payment) {
      el('payment-title').textContent = payment.mode === 'recurring' ? 'Assinatura mensal' : 'Pagamento do primeiro mês';
      el('payment-description').textContent = payment.mode === 'recurring'
        ? `Você continuará no ${payment.provider || 'provedor de pagamento'} para autorizar a cobrança mensal de ${money(plan.price)}. Confira as condições antes de confirmar.`
        : `Este pagamento cobre o primeiro mês (${money(plan.price)}). Ele não ativa uma cobrança mensal automática. As próximas mensalidades serão combinadas separadamente.`;
      el('payment-link').href = payment.url;
      el('payment-link').hidden = false;
      el('contact-link').textContent = 'Tirar dúvidas pelo WhatsApp ↗';
      el('payment-note').textContent = 'Seus dados de pagamento serão informados no ambiente do provedor. A ativação depende da confirmação do pagamento.';
    } else {
      el('payment-title').textContent = 'Pagamento online em breve';
      el('payment-description').textContent = 'Por enquanto, fale com a Nelis para combinar a contratação deste plano e a forma de pagamento.';
      el('contact-link').textContent = 'Combinar contratação pelo WhatsApp ↗';
      el('payment-note').textContent = 'Nenhuma cobrança é feita nesta página.';
    }
    if (updateUrl) {
      const url = new URL(location.href);
      url.searchParams.set('plano', key);
      history.replaceState(null, '', url);
    }
  }
  document.querySelectorAll('input[name="plano"]').forEach(radio => radio.addEventListener('change', () => showPlan(radio.value, true)));
  window.addEventListener('popstate', () => showPlan(new URLSearchParams(location.search).get('plano')));
  showPlan(new URLSearchParams(location.search).get('plano'));
})();
