'use client';

import {Form} from '@/app/components/form/Form';
import {SubmitHandler, useForm} from 'react-hook-form';
import Input from "@/app/components/form/input/Input";
import PasswordInput from "@/app/components/form/input/PasswordInput";

type FormValues = {
  username: string;
  password: string;
};

export default function SignInForm() {
  const methods = useForm<FormValues>({
    mode: 'onChange',
    defaultValues: {
      username: '',
      password: '',
    },
  });
  const {formState: {isValid, isSubmitting}} = methods;

  const onSubmit: SubmitHandler<FormValues> = (data: FormValues) => {
    console.log('Form data:', data);
  };

  return (
    <div className="flex flex-col items-start justify-center w-full gap-8">
      <div className="flex flex-col items-start justify-start gap-2">
        <h2 className="text-white text-4xl font-special font-bold">Nice to see you!</h2>
        <p className="text-gray-400 text-[15px] font-special font-semibold">
          Enter your email and password to sign in
        </p>
      </div>
      <Form<FormValues>
        methods={methods}
        onSubmit={onSubmit}
        className="w-full max-w-lg flex flex-col gap-5"
      >
        <Input
          name="username"
          type="text"
          label="Email"
          placeholder="Your email..."
          rules={{
            required: 'Email is required',
            pattern: {
              value: /^[^\s@]+@[^\s@]+\.[^\s@]+$/,
              message: 'Invalid email address',
            },
        }}
        />
        <div className="flex flex-col gap-2">
          <PasswordInput label="Password" placeholder="Your password..."/>
          <button type="button" className="self-end relative group cursor-pointer">
            <span
              className="relative text-sm bg-clip-text font-special font-semibold"
            >
              Forgot Password?
              <span
                className="absolute left-0 -bottom-0.5 h-[2px] w-0 bg-white
                          transition-all duration-500 group-hover:w-full"
              />
            </span>
          </button>
        </div>
        <button
          type="submit"
          disabled={!isValid}
          className={`
            w-full py-2.5 px-4 mt-2
            bg-theme-dodger-blue hover:bg-blue-600 disabled:bg-blue-400
            rounded-xl
            text-white text-[12px] font-special font-semibold
            transition-colors duration-300
            cursor-pointer
            disabled:cursor-not-allowed
          `}
        >
          Sign In
        </button>
        <div className="flex items-center justify-center gap-1">
          <p className="text-sm text-gray-400">
            By continuing, you agree to our
          </p>
          <button type="button" className="text-sm text-blue-400 underline hover:text-white transition-colors duration-300 cursor-pointer">
            terms of service.
          </button>
        </div>
      </Form>
    </div>
  );
}