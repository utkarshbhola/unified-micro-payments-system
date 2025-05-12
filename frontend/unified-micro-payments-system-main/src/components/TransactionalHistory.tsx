import React from 'react';

const TransactionHistory: React.FC = () => {
  const transactions = [
    { id: 1, desc: 'Sent ₹500 to @vibha', status: '✅' },
    { id: 2, desc: 'Received ₹200 from @rahul', status: '✅' },
  ];

  return (
    <div className="p-4 border rounded-xl shadow-md w-full max-w-md mx-auto mt-6">
      <h2 className="text-xl font-bold mb-4">Transaction History</h2>
      <ul>
        {transactions.map(txn => (
          <li key={txn.id} className="py-2 border-b flex justify-between">
            <span>{txn.desc}</span>
            <span>{txn.status}</span>
          </li>
        ))}
      </ul>
    </div>
  );
};

export default TransactionHistory;
