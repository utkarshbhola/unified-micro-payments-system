import React from 'react';

const UserDashboard: React.FC = () => {
  const user = {
    name: 'Utkarsh',
    upiId: 'utkarsh@umps',
    balance: 5000,
  };

  return (
    <div className="p-4 border rounded-xl shadow-md w-full max-w-md mx-auto mt-6 bg-white">
      <h2 className="text-xl font-bold mb-4">Welcome, {user.name}</h2>
      <p><strong>UPI ID:</strong> {user.upiId}</p>
      <p><strong>Balance:</strong> ₹{user.balance}</p>
    </div>
  );
};

export default UserDashboard;
