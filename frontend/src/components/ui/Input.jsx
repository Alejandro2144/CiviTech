export default function Input({ label, ...props }) {
    return (
      <div>
        <label className="block text-sm font-medium mb-1">{label}</label>
        <input
          className="w-full border px-3 py-2 rounded focus:outline-none focus:ring"
          {...props}
        />
      </div>
    )
  }
  