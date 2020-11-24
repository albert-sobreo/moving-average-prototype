Server = {
    getInventoryItems(){
        fetch('/getitems')
        .then(response => response.json())
        .then(data => app.itemOptions = data)
    },

    getInventoryPPI(itemSelect){
        payload = {
            itemSelect: itemSelect
        }

        fetch('/getinventoryppi/', {
            method: "POST",
            headers: {
                "Accept": 'application/json',
                "Content-Type": 'application/json;charset=UTF-8'
            },
            body: JSON.stringify(payload)
        })
        .then(res => res.json())
        .then(data => app.inventoryPPI = data)
    },

    pushPurchase(itemSelect, quantity, ppi, total_cost){
        payload = {
            itemSelect: itemSelect,
            quantity: quantity,
            ppi: ppi,
            total_cost: total_cost
        }

        fetch('/purchaseprocess/',{
            method: 'POST',
            headers: {
                'Accept': 'application/json',
                'Content-Type': 'application/json;charset=UTF-8'
            },
            body: JSON.stringify(payload)
        })
        .then(res=>res.json())
        .then(data=>app.giveAlerts(data))

    }
}

var app = new Vue({
    delimiters: ['[[', ']]'],
    el: '#app',
    data: {
        inventoryPPI: 0.0,
        alertMessage: '',
        quantity: 0,
        ppi: 0,
        total_cost: 0,
        itemSelect: '',
        itemOptions: [
            {
                text: '',
                value: ''
            }
        ]
    },
    methods:{
        giveAlerts(message){
            console.log(message.message, message.item, message.quantity)
            if(message.message == 'success'){
                Swal.fire({
                    title: 'Purchase Success!',
                    text: 'Your purchase of ' + message.quantity + ' ' + message.item + ((message.quantity > 1) ? 's' : '') + ' has been successful',
                    icon: 'success',
                    confirmButtonText: 'Dismiss',
                    type: 'success'
                })
            }
        },
        purchase(){
            Server.pushPurchase(this.itemSelect, this.quantity, this.ppi, this.total_cost)
            
            document.getElementById('purchaseButton').disabled = true
            this.itemSelect = ''
            this.quantity = 0
            this.ppi = 0
            this.total_cost = 0
            this.inventoryPPI = 0.0
        },
        sales(){
            Server.pushSales(this.itemSelect, this.quantity, this.total_cost)
        },
        onSelectChange0(){
            document.getElementById('purchaseButton').disabled = false
        },
        onSelectChange1(itemSelect){
            document.getElementById('purchaseButton').disabled = false
            Server.getInventoryPPI(itemSelect)
        }
    },
    watch:{
        quantity:function(val){
            this.quantity = val
            this.total_cost = (this.ppi * val).toFixed(2)
        },
        ppi:function(val){
            this.ppi = val
            this.total_cost = (val * this.quantity).toFixed(2)
        },
        inventoryPPI:function(val){
            this.inventoryPPI = val
            this.total_cost = (val * this.quantity).toFixed(2)
        }
    },
    mounted(){
        Server.getInventoryItems()
    }

})