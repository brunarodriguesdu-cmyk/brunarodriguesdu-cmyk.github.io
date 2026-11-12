/* Public checkout configuration. Never put API keys or secrets in this file.
 * Fill only with verified provider links for the matching plan and amount.
 * mode: "recurring" for an actual monthly subscription;
 *       "one_time" for payment of the first month only.
 * Keep enabled:false until provider, pricing and legal terms are ready.
 * This static redirect does not confirm payment or activate the service.
 */
window.NELIS_PAYMENTS = Object.freeze({
  assinatura: { enabled: false, url: "", mode: "", provider: "Kiwify" },
  essencial: { enabled: false, url: "", mode: "", provider: "Kiwify" },
  assistida: { enabled: false, url: "", mode: "", provider: "Kiwify" },
  presenca: { enabled: false, url: "", mode: "", provider: "Kiwify" }
});
