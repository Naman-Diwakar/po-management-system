async function loadPOs() {
    let res = await fetch("http://127.0.0.1:8000/purchase-orders");
    let data = await res.json();

    let table = document.getElementById("poTable");

    data.forEach(po => {
        let row = `
            <tr>
                <td>${po.id}</td>
                <td>${po.reference_no}</td>
                <td>${po.vendor_id}</td>
                <td>${po.total_amount}</td>
                <td>${po.status}</td>
            </tr>
        `;
        table.innerHTML += row;
    });
}

if (document.getElementById("poTable")) {
    loadPOs();
}

// Load vendors
async function loadVendors() {
    let res = await fetch("http://127.0.0.1:8000/vendors");
    let vendors = await res.json();

    let select = document.getElementById("vendor");

    vendors.forEach(v => {
        select.innerHTML += `<option value="${v.id}">${v.name}</option>`;
    });
}

// Load products
async function loadProducts() {
    let res = await fetch("http://127.0.0.1:8000/products");
    return await res.json();
}

// Add row
async function addRow() {
    let products = await loadProducts();

    let options = "";
    products.forEach(p => {
        options += `<option value="${p.id}" data-price="${p.unit_price}">${p.name}</option>`;
    });

    let row = `
        <tr>
            <td>
                <select class="product form-control" onchange="updatePrice(this)">
                    ${options}
                </select>
            </td>
            <td>
                <input type="number" class="qty form-control" value="1" oninput="calculateTotal()">
            </td>
            <td>
                <input type="number" class="price form-control" value="0" oninput="calculateTotal()">
            </td>
            <td>
                <button class="btn btn-danger" onclick="this.closest('tr').remove(); calculateTotal();">X</button>
            </td>
        </tr>
    `;

    document.getElementById("items").innerHTML += row;
}

// Submit PO
async function submitPO() {
    let ref = document.getElementById("ref").value;
    let vendor_id = document.getElementById("vendor").value;

    let rows = document.querySelectorAll("#items tr");

    let items = [];

    rows.forEach(row => {
        let product_id = row.querySelector(".product").value;
        let quantity = row.querySelector(".qty").value;
        let price = row.querySelector(".price").value;

        items.push({
            product_id: parseInt(product_id),
            quantity: parseInt(quantity),
            price: parseFloat(price)
        });
    });

    let data = {
        reference_no: ref,
        vendor_id: parseInt(vendor_id),
        items: items
    };

    await fetch("http://127.0.0.1:8000/purchase-orders", {
        method: "POST",
        headers: {
            "Content-Type": "application/json"
        },
        body: JSON.stringify(data)
    });

    alert("✅ Purchase Order Created Successfully!");
    window.location.href = "index.html";
}

if (document.getElementById("vendor")) {
    loadVendors();
}

function updatePrice(select) {
    let price = select.options[select.selectedIndex].getAttribute("data-price");
    let row = select.closest("tr");
    row.querySelector(".price").value = price;

    calculateTotal(); // update total automatically
}

function calculateTotal() {
    let rows = document.querySelectorAll("#items tr");
    let total = 0;

    rows.forEach(row => {
        let qty = row.querySelector(".qty").value;
        let price = row.querySelector(".price").value;

        total += qty * price;
    });

    let tax = total * 0.05;
    let final = total + tax;

    document.getElementById("total").innerText = final.toFixed(2);
}