// ===== CONFIGURATION =====
const API_URL = 'http://localhost:5000/api';

// ===== ÉTAT GLOBAL =====
let cart = [];
let clientInfo = null;
let allProducts = [];

// ===== INITIALISATION =====
document.addEventListener('DOMContentLoaded', () => {
    setupEvents();
    showHome();
});

// ===== ÉVÉNEMENTS =====
function setupEvents() {
    // Accueil
    document.getElementById('recommendations-btn').addEventListener('click', showRecommendations);
    document.getElementById('order-btn').addEventListener('click', showCheckout);

    // Checkout
    document.getElementById('checkout-form').addEventListener('submit', submitCheckout);
    document.getElementById('back-checkout').addEventListener('click', showHome);

    // Recommandations
    document.getElementById('back-recommendations').addEventListener('click', showHome);

    // Menu
    document.getElementById('back-menu').addEventListener('click', showHome);
    document.querySelectorAll('.category-btn').forEach(btn => {
        btn.addEventListener('click', filterByCategory);
    });

    // Panier
    document.getElementById('cart-btn').addEventListener('click', showCart);
    document.getElementById('back-cart').addEventListener('click', showMenu);

    // Confirmation
    document.getElementById('back-home').addEventListener('click', showHome);
}

// ===== NAVIGATION =====
function hideAllPages() {
    document.getElementById('home-page').classList.add('hidden');
    document.getElementById('checkout-page').classList.add('hidden');
    document.getElementById('recommendations-page').classList.add('hidden');
    document.getElementById('menu-page').classList.add('hidden');
    document.getElementById('cart-page').classList.add('hidden');
    document.getElementById('confirmation-page').classList.add('hidden');
}

function showHome() {
    hideAllPages();
    document.getElementById('home-page').classList.remove('hidden');
}

function showCheckout() {
    hideAllPages();
    document.getElementById('checkout-page').classList.remove('hidden');
}

async function showMenu() {
    hideAllPages();
    document.getElementById('menu-page').classList.remove('hidden');
    
    // Récupérer les produits
    try {
        const response = await fetch(`${API_URL}/menu`);
        const data = await response.json();
        allProducts = data.products;
        displayProducts(allProducts);
        // Réinitialiser les catégories
        document.querySelectorAll('.category-btn').forEach(btn => {
            btn.classList.remove('active');
        });
        document.querySelector('.category-btn[data-category="all"]').classList.add('active');
    } catch (error) {
        console.error('Erreur :', error);
        document.getElementById('menu-content').innerHTML = '<p>Erreur de connexion à l\'API</p>';
    }
}

function showRecommendations() {
    hideAllPages();
    document.getElementById('recommendations-page').classList.remove('hidden');
    
    // TODO: Ajouter formulaire recommandations ici
    document.getElementById('recommendations-content').innerHTML = `
        <p style="text-align: center; color: #999;">Formulaire recommandations à venir</p>
    `;
}

async function showCart() {
    if (cart.length === 0) {
        alert('Votre panier est vide');
        return;
    }

    hideAllPages();
    document.getElementById('cart-page').classList.remove('hidden');
    displayCart();
}

// ===== CHECKOUT =====
function submitCheckout(e) {
    e.preventDefault();

    clientInfo = {
        name: document.getElementById('name').value,
        phone: document.getElementById('phone').value,
        mode: document.querySelector('input[name="mode"]:checked').value
    };

    console.log('Client info saved:', clientInfo);
    showMenu();
}

// ===== MENU =====
function displayProducts(products) {
    const container = document.getElementById('menu-content');
    container.innerHTML = '';

    if (products.length === 0) {
        container.innerHTML = '<p>Aucun produit disponible</p>';
        return;
    }

    const grid = document.createElement('div');
    grid.className = 'products-grid';

    products.forEach(product => {
        const card = document.createElement('div');
        card.className = 'product-card';
        card.innerHTML = `
            <img src="${product.image}" alt="${product.name}" class="product-image" 
                 onerror="this.src='https://via.placeholder.com/200?text=${encodeURIComponent(product.name)}'">
            <div class="product-info">
                <div class="product-name">${product.name}</div>
                <div class="product-category">${product.category}</div>
                <div class="product-price">${product.price.toFixed(2)}€</div>
                <button class="btn-add" onclick="addToCart(${product.id}, '${product.name.replace(/'/g, "\\'")}', ${product.price})">
                    Ajouter
                </button>
            </div>
        `;
        grid.appendChild(card);
    });

    container.appendChild(grid);
}

function filterByCategory(e) {
    const category = e.target.dataset.category;
    
    // Activer le bouton
    document.querySelectorAll('.category-btn').forEach(btn => {
        btn.classList.remove('active');
    });
    e.target.classList.add('active');

    // Filtrer
    if (category === 'all') {
        displayProducts(allProducts);
    } else {
        const filtered = allProducts.filter(p => p.category === category);
        displayProducts(filtered);
    }
}

// ===== PANIER =====
function addToCart(id, name, price) {
    if (!clientInfo) {
        alert('Veuillez d\'abord remplir vos informations de commande');
        showCheckout();
        return;
    }

    cart.push({ id, name, price });
    updateCartCount();
    alert(`${name} ajouté au panier !`);
}

function updateCartCount() {
    document.getElementById('cart-count').textContent = cart.length;
}

function displayCart() {
    const container = document.getElementById('cart-content');
    container.innerHTML = '';

    if (cart.length === 0) {
        container.innerHTML = '<p>Panier vide</p>';
        return;
    }

    // Infos client
    const clientDiv = document.createElement('div');
    clientDiv.className = 'cart-summary';
    clientDiv.innerHTML = `
        <h3>Informations de commande</h3>
        <p><strong>Nom :</strong> ${clientInfo.name}</p>
        <p><strong>Téléphone :</strong> ${clientInfo.phone}</p>
        <p><strong>Mode :</strong> ${clientInfo.mode === 'sur_place' ? 'Sur place' : 'À emporter'}</p>
    `;
    container.appendChild(clientDiv);

    // Articles du panier
    const itemsDiv = document.createElement('div');
    itemsDiv.className = 'cart-summary';
    itemsDiv.innerHTML = '<h3>Vos articles</h3>';

    let total = 0;
    cart.forEach((item, index) => {
        const itemDiv = document.createElement('div');
        itemDiv.className = 'cart-item';
        itemDiv.innerHTML = `
            <div class="cart-item-info">
                <div class="cart-item-name">${item.name}</div>
                <div class="cart-item-price">${item.price.toFixed(2)}€</div>
            </div>
            <button class="btn-remove" onclick="removeFromCart(${index})">Retirer</button>
        `;
        itemsDiv.appendChild(itemDiv);
        total += item.price;
    });

    container.appendChild(itemsDiv);

    // Total
    const totalDiv = document.createElement('div');
    totalDiv.className = 'cart-summary';
    totalDiv.innerHTML = `
        <div class="cart-total">Total : ${total.toFixed(2)}€</div>
    `;
    container.appendChild(totalDiv);

    // Bouton validation
    const btnDiv = document.createElement('div');
    btnDiv.innerHTML = `
        <button class="btn-primary btn-large" onclick="validateOrder()">
            Valider la commande
        </button>
    `;
    container.appendChild(btnDiv);
}

function removeFromCart(index) {
    cart.splice(index, 1);
    updateCartCount();
    if (cart.length === 0) {
        showMenu();
    } else {
        displayCart();
    }
}

// ===== COMMANDE =====
function validateOrder() {
    if (cart.length === 0) {
        alert('Panier vide');
        return;
    }

    // Générer numéro commande
    const orderNumber = Math.floor(Math.random() * 10000) + 1000;
    
    // Afficher confirmation
    showConfirmation(orderNumber);
}

function showConfirmation(orderNumber) {
    hideAllPages();
    document.getElementById('confirmation-page').classList.remove('hidden');

    document.getElementById('order-number').textContent = `#${orderNumber}`;

    let detailsHTML = `
        <p><strong>Nom :</strong> ${clientInfo.name}</p>
        <p><strong>Téléphone :</strong> ${clientInfo.phone}</p>
        <p><strong>Mode :</strong> ${clientInfo.mode === 'sur_place' ? 'Sur place' : 'À emporter'}</p>
        <hr style="margin: 15px 0;">
        <p><strong>Articles commandés :</strong></p>
    `;

    let total = 0;
    cart.forEach(item => {
        detailsHTML += `<p>- ${item.name} : ${item.price.toFixed(2)}€</p>`;
        total += item.price;
    });

    detailsHTML += `<hr style="margin: 15px 0;"><p><strong>Total : ${total.toFixed(2)}€</strong></p>`;

    document.getElementById('confirmation-details').innerHTML = detailsHTML;

    // Réinitialiser
    cart = [];
    updateCartCount();
}

// Afficher accueil au démarrage
showHome();