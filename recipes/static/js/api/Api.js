
class Api {
  constructor(apiUrl) {
    this.apiUrl = apiUrl;
    this.csrftoken = document.querySelector('[name=csrfmiddlewaretoken]').value;
  }
  getPurchases() {
    return fetch(`${this.apiUrl}/purchases/`, {
      headers: {
        'Content-Type': 'application/json',
        'X-CSRFToken': this.csrftoken
      }
    })
      .then(e => {
        if (e.ok) {
          return e.json()
        }
        return Promise.reject(e.statusText)
      })
  }
  addPurchases(id) {
    return fetch(`${this.apiUrl}/purchases/`, {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json',
        'X-CSRFToken': this.csrftoken
      },
      body: JSON.stringify({
        recipe: id
      })
    })
      .then(e => {
        if (e.ok) {
          return e.json()
        }
        return Promise.reject(e.statusText)
      })
  }
  removePurchases(id) {
    return fetch(`${this.apiUrl}/purchases/${id}/`, {
      method: 'DELETE',
      headers: {
        'Content-Type': 'application/json',
        'X-CSRFToken': this.csrftoken
      }
    })
  }
  addSubscriptions(id) {
    return fetch(`${this.apiUrl}/subscriptions/`, {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json',
        'X-CSRFToken': this.csrftoken
      },
      body: JSON.stringify({
        author: id
      })
    })
      .then(e => {
        if (e.ok) {
          return e.json()
        }
        return Promise.reject(e.statusText)
      })
  }
  removeSubscriptions(id) {
    return fetch(`${this.apiUrl}/subscriptions/${id}/`, {
      method: 'DELETE',
      headers: {
        'Content-Type': 'application/json',
        'X-CSRFToken': this.csrftoken
      }
    })
  }
  addFavorites(id) {
    return fetch(`${this.apiUrl}/favorites/`, {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json',
        'X-CSRFToken': this.csrftoken
      },
      body: JSON.stringify({
        recipe: id
      })
    })
      .then(e => {
        if (e.ok) {
          return e.json()
        }
        return Promise.reject(e.statusText)
      })
  }
  removeFavorites(id) {
    return fetch(`${this.apiUrl}/favorites/${id}/`, {
      method: 'DELETE',
      headers: {
        'Content-Type': 'application/json',
        'X-CSRFToken': this.csrftoken
      }
    })
  }
  getIngredients(text) {
    return fetch(`${this.apiUrl}/ingredients/?search=${text}`, {
      headers: {
        'Content-Type': 'application/json',
        'X-CSRFToken': this.csrftoken
      }
    })
      .then(e => {
        if (e.ok) {
          return e.json()
        }
        return Promise.reject(e.statusText)
      })
  }
}
