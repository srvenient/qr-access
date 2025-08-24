import {useFormContext} from "react-hook-form";
import {HTMLInputTypeAttribute} from 'react';
import {ExclamationCircleIcon} from "@heroicons/react/24/solid";

type InputProps = {
  name: string;
  type?: HTMLInputTypeAttribute | undefined;
  placeholder?: string;
  label?: string;
  rules?: object;
  className?: string;
};


export default function Input({name, type, placeholder = '', label, rules, className}: InputProps) {
  const {
    register,
    formState: {errors},
  } = useFormContext();

  return (
    <div className="flex flex-col gap-3">
      {label && (
        <label
          htmlFor={name}
          className="block text-sm text-white font-special font-semibold"
        >
          {label}
        </label>
      )}
      <div
        className={`
          relative rounded-2xl p-[1px] transition-colors duration-150
        `}
        style={{
          background: "radial-gradient(94.43% 69.43%, rgb(255,255,255) 0%, rgba(255,255,255,0) 100%)",
        }}
      >
        <input
          type={type}
          placeholder={placeholder}
          className={`
            w-full py-2.5 px-4
            bg-[rgb(15,21,53)]
            rounded-2xl
            border-[0.5px] border-[rgb(74,85,104)]
            text-sm  
            placeholder:text-[rgb(200,200,210)] placeholder:text-[12px] placeholder:font-light placeholder:opacity-15
            outline-none
            focus:ring-1 focus:ring-blue-500 focus:caret-blue-500
            ${errors[name] ? "ring-1 ring-red-500" : ""}
            peer
            transition-all duration-150
          `}
          {...register(name, rules)}
        />
      </div>
    </div>
  );
}