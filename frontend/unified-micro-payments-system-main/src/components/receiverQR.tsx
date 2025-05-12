import React from 'react';

const ReceiveQR: React.FC = () => {
  return (
    <div className="p-4 border rounded-xl shadow-md w-full max-w-md mx-auto mt-6">
      <h2 className="text-xl font-bold mb-4">Receive via QR</h2>
      <div className="w-48 h-48 bg-gray-300 mx-auto mb-4 flex items-center justify-center text-gray-600">
        QR Placeholder
      </div>
      <p className="text-center">Scan this QR to pay <strong>@utkarsh</strong></p>
    </div>
  );
};

export default ReceiveQR;
