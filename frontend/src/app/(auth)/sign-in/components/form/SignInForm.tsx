'use client';

import {Form} from '@/app/components/form/Form';
import {SubmitHandler, useForm} from 'react-hook-form';
import Input from "@/app/components/form/input/Input";
import PasswordInput from "@/app/components/form/input/PasswordInput";
import {useRouter} from "next/navigation";
import {authHttpClient} from "@/app/(auth)/sign-in/lib/auth.http-client";

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
  const {setError, formState: {isValid, isSubmitting}} = methods;
  const router = useRouter();

  const onSubmit: SubmitHandler<FormValues> = async (data: FormValues): Promise<void> => {
    try {
      const success = await authHttpClient.login(data.username, data.password);
      if (success) {
        router.replace("/dashboard");
      }
    } catch (error: unknown) {
      if (error instanceof Error) {
        setError("username", { message: error.message }); // o "password" según el caso
      } else {
        console.error("Unexpected error", error);
      }
    }
  }

  return (
    <div className="flex flex-col items-start justify-center w-full gap-8">
      <div className="flex flex-col items-start justify-start gap-2">
        <h2 className="text-white text-4xl font-special font-bold">Nice to see you!</h2>
        <p className="text-gray-400 text-[15px] font-special font-semibold">
          Enter your email and password to sign in
        </p>
      </div>
      {}
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
              className="relative text-[13.5px] bg-clip-text font-special font-semibold"
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
          disabled={!isValid || isSubmitting}
          className={`
            w-full py-2.5 px-4 mt-2
            bg-theme-dodger-blue enabled:hover:bg-blue-600 
            rounded-xl
            text-white text-[10.5px]  font-semibold
            transition-colors duration-300
            cursor-pointer
            disabled:cursor-not-allowed
          `}
        >
          SIGN IN
        </button>
        <div className="flex items-center justify-center gap-1">
          <p className="text-sm text-gray-400">
            By continuing, you agree to our
          </p>
          <button type="button"
                  className="text-sm text-blue-400 underline hover:text-white transition-colors duration-300 cursor-pointer">
            terms of service.
          </button>
        </div>
      </Form>
    </div>
  );
}