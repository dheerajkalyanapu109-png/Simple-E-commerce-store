// Add to cart without a page reload; falls back to a normal form post if fetch fails.
document.querySelectorAll("form[data-add]").forEach(form => {
  form.addEventListener("submit", async e => {
    e.preventDefault();
    try {
      const res = await fetch(form.action, {method: "POST", body: new FormData(form), headers: {"x-requested-with": "fetch"}});
      if (!res.ok) throw new Error();
      const data = await res.json();
      document.getElementById("cart-count").textContent = data.count;
      const t = document.getElementById("toast");
      t.textContent = data.name + " added to cart";
      t.classList.add("show"); setTimeout(() => t.classList.remove("show"), 1800);
    } catch { form.submit(); }
  });
});
