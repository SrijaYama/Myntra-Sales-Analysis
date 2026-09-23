import { readFileSync } from "fs";

const lines = readFileSync(".bob/tmp/office-dumps/Myntra_Sales_Dataset-02181678/data.txt", "utf8").trim().split("\n");

const colMap = {};
let totalSales = 0, totalProfit = 0, totalQty = 0, totalDiscount = 0;
let totalRating = 0, ratingCount = 0;
const orderIds = new Set();
const salesByCategory = {}, salesByCity = {}, salesByGender = {}, salesByCustType = {}, salesByPayment = {}, salesByProduct = {};
const ordersByStatus = {}, ordersByPayment = {};
const monthlySales = {}, monthlyProfit = {};

for (const line of lines) {
    if (!line.trim()) continue;
    const tabIdx = line.indexOf("\t");
    if (tabIdx === -1) continue;
    const header = line.slice(0, tabIdx);
    const cellPart = line.slice(tabIdx + 1);

    const rowMatch = header.match(/row\[(\d+)\]/);
    if (!rowMatch) continue;
    const rowNum = parseInt(rowMatch[1]);

    const record = {};
    for (const cell of cellPart.split("\t")) {
        const eqIdx = cell.indexOf("=");
        if (eqIdx === -1) continue;
        const key = cell.slice(0, eqIdx);
        const val = cell.slice(eqIdx + 1);
        const col = key.replace(/\d+$/, "");
        record[col] = val;
    }

    if (rowNum === 1) {
        for (const [col, name] of Object.entries(record)) colMap[col] = name;
        console.log("Column map:", colMap);
        continue;
    }

    // Columns: A=Order ID, B=Order Date, C=City, D=Customer Type, E=Gender, F=Product, G=Category, H=Quantity, I=Unit Price, J=Discount %, K=Discount Amount, L=Payment Method, M=Order Status, N=Rating, O=Sales, P=Cost, Q=Profit
    const orderId = record["A"] ?? "";
    const city = record["C"] ?? "Unknown";
    const custType = record["D"] ?? "Unknown";
    const gender = record["E"] ?? "Unknown";
    const product = record["F"] ?? "Unknown";
    const category = record["G"] ?? "Unknown";
    const qty = parseFloat(record["H"] ?? "0") || 0;
    const discPct = parseFloat(record["J"] ?? "0") || 0;
    const discAmt = parseFloat(record["K"] ?? "0") || 0;
    const payment = record["L"] ?? "Unknown";
    const status = record["M"] ?? "Unknown";
    const rating = parseFloat(record["N"] ?? "0") || 0;
    const sales = parseFloat(record["O"] ?? "0") || 0;
    const profit = parseFloat(record["Q"] ?? "0") || 0;
    const orderDate = record["B"] ?? "";

    // Parse month-year from date (format may be YYYY-MM-DD or similar)
    let monthYear = "Unknown";
    if (orderDate) {
        // Try to parse date - format is likely a serial or string
        const dateStr = orderDate.trim();
        if (dateStr.match(/^\d{4}-\d{2}/)) {
            monthYear = dateStr.slice(0, 7);
        } else if (dateStr.match(/^\d{1,2}\/\d{1,2}\/\d{4}/)) {
            const parts = dateStr.split("/");
            monthYear = `${parts[2]}-${parts[0].padStart(2,"0")}`;
        }
    }

    orderIds.add(orderId);
    totalSales += sales;
    totalProfit += profit;
    totalQty += qty;
    totalDiscount += discAmt;
    if (rating > 0) { totalRating += rating; ratingCount++; }

    salesByCategory[category] = (salesByCategory[category] ?? 0) + sales;
    salesByCity[city] = (salesByCity[city] ?? 0) + sales;
    salesByGender[gender] = (salesByGender[gender] ?? 0) + sales;
    salesByCustType[custType] = (salesByCustType[custType] ?? 0) + sales;
    salesByPayment[payment] = (salesByPayment[payment] ?? 0) + sales;
    salesByProduct[product] = (salesByProduct[product] ?? 0) + sales;
    ordersByStatus[status] = (ordersByStatus[status] ?? 0) + 1;
    ordersByPayment[payment] = (ordersByPayment[payment] ?? 0) + 1;
    monthlySales[monthYear] = (monthlySales[monthYear] ?? 0) + sales;
    monthlyProfit[monthYear] = (monthlyProfit[monthYear] ?? 0) + profit;
}

const totalOrders = orderIds.size;
const avgOrderVal = totalOrders > 0 ? totalSales / totalOrders : 0;
const avgRating = ratingCount > 0 ? totalRating / ratingCount : 0;
const profitMargin = totalSales > 0 ? (totalProfit / totalSales * 100) : 0;

console.log("\n=== KPI SUMMARY ===");
console.log(`Total Sales: ₹${totalSales.toFixed(2)}`);
console.log(`Total Profit: ₹${totalProfit.toFixed(2)}`);
console.log(`Profit Margin: ${profitMargin.toFixed(2)}%`);
console.log(`Total Quantity: ${totalQty}`);
console.log(`Total Orders: ${totalOrders}`);
console.log(`Avg Order Value: ₹${avgOrderVal.toFixed(2)}`);
console.log(`Avg Rating: ${avgRating.toFixed(2)}`);
console.log(`Total Discount: ₹${totalDiscount.toFixed(2)}`);

console.log("\n=== SALES BY CATEGORY ===");
Object.entries(salesByCategory).sort((a,b)=>b[1]-a[1]).forEach(([k,v])=>console.log(`${k}: ₹${v.toFixed(2)}`));

console.log("\n=== TOP 10 PRODUCTS ===");
Object.entries(salesByProduct).sort((a,b)=>b[1]-a[1]).slice(0,10).forEach(([k,v])=>console.log(`${k}: ₹${v.toFixed(2)}`));

console.log("\n=== SALES BY CITY ===");
Object.entries(salesByCity).sort((a,b)=>b[1]-a[1]).forEach(([k,v])=>console.log(`${k}: ₹${v.toFixed(2)}`));

console.log("\n=== SALES BY GENDER ===");
Object.entries(salesByGender).sort((a,b)=>b[1]-a[1]).forEach(([k,v])=>console.log(`${k}: ₹${v.toFixed(2)}`));

console.log("\n=== SALES BY CUSTOMER TYPE ===");
Object.entries(salesByCustType).sort((a,b)=>b[1]-a[1]).forEach(([k,v])=>console.log(`${k}: ₹${v.toFixed(2)}`));

console.log("\n=== SALES BY PAYMENT METHOD ===");
Object.entries(salesByPayment).sort((a,b)=>b[1]-a[1]).forEach(([k,v])=>console.log(`${k}: ₹${v.toFixed(2)}`));

console.log("\n=== ORDER COUNT BY PAYMENT METHOD ===");
Object.entries(ordersByPayment).sort((a,b)=>b[1]-a[1]).forEach(([k,v])=>console.log(`${k}: ${v}`));

console.log("\n=== ORDER STATUS ===");
Object.entries(ordersByStatus).sort((a,b)=>b[1]-a[1]).forEach(([k,v])=>console.log(`${k}: ${v}`));

console.log("\n=== MONTHLY SALES ===");
Object.entries(monthlySales).sort((a,b)=>a[0].localeCompare(b[0])).forEach(([k,v])=>console.log(`${k}: ₹${v.toFixed(2)} | Profit: ₹${(monthlyProfit[k]??0).toFixed(2)}`));
