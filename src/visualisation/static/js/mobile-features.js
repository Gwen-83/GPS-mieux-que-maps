// ===== MOBILE FEATURES =====
// Gestion de l'historique, favoris, et partage

class MobileFeatures {
    constructor() {
        this.history = this.loadFromStorage('gps_history') || [];
        this.favorites = this.loadFromStorage('gps_favorites') || [];
        this.maxHistoryItems = 20;
        this.initEventListeners();
    }

    initEventListeners() {
        const menuBtn = document.getElementById('btn-menu');
        const historyBtn = document.getElementById('btn-history');
        const shareBtn = document.getElementById('btn-share');
        const favoriteBtn = document.getElementById('btn-favorite');

        if (menuBtn) menuBtn.addEventListener('click', () => this.openModal('menu-modal'));
        if (historyBtn) historyBtn.addEventListener('click', () => this.openHistoryModal());
        if (shareBtn) shareBtn.addEventListener('click', () => this.shareRoute());
        if (favoriteBtn) favoriteBtn.addEventListener('click', () => this.promptAddToFavorites());

        // Boutons du menu
        document.getElementById('btn-favorites')?.addEventListener('click', () => {
            this.openFavoritesModal();
            this.closeModal('menu-modal');
        });

        document.getElementById('btn-settings')?.addEventListener('click', () => {
            this.openModal('settings-modal');
            this.closeModal('menu-modal');
        });

        document.getElementById('btn-about')?.addEventListener('click', () => {
            this.openModal('about-modal');
            this.closeModal('menu-modal');
        });

        // Fermer les modals
        document.querySelectorAll('.close-modal-btn').forEach(btn => {
            btn.addEventListener('click', (e) => {
                const modal = e.target.closest('.modal-overlay');
                if (modal) modal.style.display = 'none';
            });
        });

        // Fermer modal au clic sur overlay
        document.querySelectorAll('.modal-overlay').forEach(overlay => {
            overlay.addEventListener('click', (e) => {
                if (e.target === overlay) overlay.style.display = 'none';
            });
        });
    }

    // ===== HISTORIQUE =====
    addToHistory(depart, arrivee, distance, temps) {
        const item = {
            id: Date.now(),
            depart,
            arrivee,
            distance,
            temps,
            date: new Date().toLocaleString('fr-FR', {
                year: 'numeric',
                month: '2-digit',
                day: '2-digit',
                hour: '2-digit',
                minute: '2-digit'
            })
        };

        this.history.unshift(item);
        if (this.history.length > this.maxHistoryItems) {
            this.history.pop();
        }

        this.saveToStorage('gps_history', this.history);
    }

    openHistoryModal() {
        const historyList = document.getElementById('history-list');

        if (this.history.length === 0) {
            historyList.innerHTML = '<p class="empty-state">Aucun trajet dans l\'historique</p>';
        } else {
            historyList.innerHTML = this.history.map(item => `
                <div class="history-item">
                    <div class="history-item-content">
                        <div class="history-item-route">${item.depart} → ${item.arrivee}</div>
                        <div class="history-item-info">
                            <span>${item.distance} km • ${item.temps}</span>
                            <span class="history-item-date">${item.date}</span>
                        </div>
                    </div>
                    <div class="history-item-action">
                        <button class="small-btn" title="Charger" onclick="mobileFeatures.loadRouteFromHistory(${item.id})">
                            <i class="fas fa-redo"></i>
                        </button>
                        <button class="small-btn" title="Supprimer" onclick="mobileFeatures.deleteFromHistory(${item.id})">
                            <i class="fas fa-trash"></i>
                        </button>
                    </div>
                </div>
            `).join('');
        }

        this.openModal('history-modal');
    }

    async loadRouteFromHistory(param) {
        let item;
        if (typeof param === 'object') {
            // Pour favoris, param est {depart, arrivee}
            item = param;
        } else {
            // Pour historique, param est id
            item = this.history.find(h => h.id === param);
        }
        if (!item) return;

        try {
            // Rechercher l'ID pour le départ
            const departResponse = await fetch('/api/recherche_ville', {
                method: 'POST',
                headers: { 'Content-Type': 'application/json' },
                body: JSON.stringify({ nom: item.depart })
            });
            const departVilles = await departResponse.json();
            const departVille = departVilles.find(v => v.nom === item.depart) || departVilles[0];
            
            if (departVille) {
                document.getElementById('depart_input').value = departVille.nom;
                document.getElementById('depart_id').value = departVille.id;
                document.getElementById('depart_status').innerHTML = "<span style='color: #27ae60;'>✅ Validé</span>";
            }

            // Rechercher l'ID pour l'arrivée
            const arriveeResponse = await fetch('/api/recherche_ville', {
                method: 'POST',
                headers: { 'Content-Type': 'application/json' },
                body: JSON.stringify({ nom: item.arrivee })
            });
            const arriveeVilles = await arriveeResponse.json();
            const arriveeVille = arriveeVilles.find(v => v.nom === item.arrivee) || arriveeVilles[0];
            
            if (arriveeVille) {
                document.getElementById('arrivee_input').value = arriveeVille.nom;
                document.getElementById('arrivee_id').value = arriveeVille.id;
                document.getElementById('arrivee_status').innerHTML = "<span style='color: #27ae60;'>✅ Validé</span>";
            }

            this.closeModal('history-modal');
            showToast('Trajet chargé', 'success');

            // Auto-lancer le calcul automatiquement après chargement
            setTimeout(() => document.getElementById('btn-calcul').click(), 300);
        } catch (error) {
            console.error('Erreur lors du chargement du trajet:', error);
            showToast('Erreur lors du chargement du trajet', 'error');
        }
    }

    deleteFromHistory(id) {
        this.history = this.history.filter(h => h.id !== id);
        this.saveToStorage('gps_history', this.history);
        this.openHistoryModal();
        showToast('Trajet supprimé', 'info');
    }

    // ===== FAVORIS =====
    openFavoritesModal() {
        const favoritesList = document.getElementById('favorites-list');

        if (this.favorites.length === 0) {
            favoritesList.innerHTML = '<p class="empty-state">Aucun trajet en favoris</p>';
        } else {
            favoritesList.innerHTML = this.favorites.map(item => `
                <div class="favorite-item">
                    <div class="favorite-item-content">
                        <div class="history-item-route">${item.nom}</div>
                        <div class="history-item-info">
                            ${item.depart} → ${item.arrivee}
                        </div>
                    </div>
                    <div class="favorite-item-action">
                        <button class="small-btn" title="Charger" onclick="mobileFeatures.loadRouteFromFavorite(${item.id})">
                            <i class="fas fa-redo"></i>
                        </button>
                        <button class="small-btn" title="Supprimer" onclick="mobileFeatures.removeFromFavorites(${item.id})">
                            <i class="fas fa-star"></i>
                        </button>
                    </div>
                </div>
            `).join('');
        }

        this.openModal('favorites-modal');
    }

    addToFavorites(depart, arrivee) {
        const nom = prompt(`Nommer ce trajet:\n${depart} → ${arrivee}`);
        if (!nom || nom.trim() === '') return;

        const item = {
            id: Date.now(),
            nom: nom.trim(),
            depart,
            arrivee
        };

        this.favorites.push(item);
        this.saveToStorage('gps_favorites', this.favorites);
        showToast(`✅ "${nom}" ajouté aux favoris`, 'success');
    }

    promptAddToFavorites() {
        const depart = document.getElementById('depart_input').value;
        const arrivee = document.getElementById('arrivee_input').value;

        if (!depart || !arrivee) {
            showToast('Veuillez calculer un itinéraire d\'abord', 'warning');
            return;
        }

        this.addToFavorites(depart, arrivee);
    }

    loadRouteFromFavorite(id) {
        const item = this.favorites.find(f => f.id === id);
        if (item) {
            this.loadRouteFromHistory({ depart: item.depart, arrivee: item.arrivee });
            this.closeModal('favorites-modal');
        }
    }

    removeFromFavorites(id) {
        this.favorites = this.favorites.filter(f => f.id !== id);
        this.saveToStorage('gps_favorites', this.favorites);
        this.openFavoritesModal();
        showToast('Favoris supprimé', 'info');
    }

    clearHistory() {
        if (confirm('Êtes-vous sûr de vouloir effacer tout l\'historique?')) {
            this.history = [];
            this.saveToStorage('gps_history', this.history);
            this.openHistoryModal();
            showToast('Historique effacé', 'info');
        }
    }

    clearFavorites() {
        if (confirm('Êtes-vous sûr de vouloir effacer tous les favoris?')) {
            this.favorites = [];
            this.saveToStorage('gps_favorites', this.favorites);
            this.openFavoritesModal();
            showToast('Favoris effacés', 'info');
        }
    }

    // ===== PARTAGE =====
    shareRoute() {
        const depart = document.getElementById('depart_input').value;
        const arrivee = document.getElementById('arrivee_input').value;
        const distance = document.getElementById('res_dist').textContent;
        const temps = document.getElementById('res_temps').textContent;

        if (!depart || !arrivee) {
            showToast('Veuillez calculer un itinéraire d\'abord', 'warning');
            return;
        }

        const text = `GPS du touriste:\n${depart} → ${arrivee}\nDistance: ${distance}\nTemps: ${temps}`;

        if (navigator.share) {
            navigator.share({
                title: 'Itinéraire GPS',
                text: text,
                url: window.location.href
            }).catch(err => console.log('Erreur partage:', err));
        } else {
            // Fallback: copier dans le presse-papier
            navigator.clipboard.writeText(text).then(() => {
                showToast('Itinéraire copié', 'success');
            });
        }
    }

    // ===== UTILITAIRES =====
    formatTime(minutes) {
        if (minutes < 60) return `${Math.round(minutes)} min`;
        const hours = Math.floor(minutes / 60);
        const mins = Math.round(minutes % 60);
        return `${hours}h ${mins}min`;
    }

    openModal(modalId) {
        document.getElementById(modalId).style.display = 'flex';
    }

    closeModal(modalId) {
        document.getElementById(modalId).style.display = 'none';
    }

    saveToStorage(key, data) {
        try {
            localStorage.setItem(key, JSON.stringify(data));
        } catch (e) {
            console.warn('LocalStorage indisponible:', e);
        }
    }

    loadFromStorage(key) {
        try {
            const data = localStorage.getItem(key);
            return data ? JSON.parse(data) : null;
        } catch (e) {
            console.warn('Erreur chargement localStorage:', e);
            return null;
        }
    }
}

// Initialiser au chargement du DOM
let mobileFeatures;
document.addEventListener('DOMContentLoaded', () => {
    if (!mobileFeatures) {
        mobileFeatures = new MobileFeatures();
    }
});
