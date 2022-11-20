db = db.getSiblingDB('financeFollower')

db.createCollection('markets')

db.markets.insertMany([
    {
        name: 'Stocks'
    },
    {
        name: 'Fiis'
    }
])