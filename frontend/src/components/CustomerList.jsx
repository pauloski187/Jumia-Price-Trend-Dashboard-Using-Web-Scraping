import React from 'react'

export default function CustomerList() {
  const rows = [
    { id: '1', name: 'Sample Product', price: 100, currency: 'NGN' },
  ]
  return (
    <div>
      <h2>Products</h2>
      <table border="1" cellPadding={6}>
        <thead>
          <tr>
            <th>ID</th>
            <th>Name</th>
            <th>Price</th>
            <th>Currency</th>
          </tr>
        </thead>
        <tbody>
          {rows.map(r => (
            <tr key={r.id}>
              <td>{r.id}</td>
              <td>{r.name}</td>
              <td>{r.price}</td>
              <td>{r.currency}</td>
            </tr>
          ))}
        </tbody>
      </table>
    </div>
  )
}
