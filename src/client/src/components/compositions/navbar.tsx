import Image from 'next/image';
import Bitcoin from '@/assets/Bitcoin.png';
import DataTypeSelect from '@/components/compositions/data-type-select';

const Navbar = () => {
  return (
    <nav className="flex items-center justify-between gap-2 py-4 px-8 text-white bg-neutral-800 shadow-lg">
      <div className={'flex items-center gap-2'}>
        <Image src={Bitcoin} alt={'Bitcoin'} width={48} height={48} />
        <h1 className="text-2xl font-bold">Bitcoin Hodl Prophet</h1>
      </div>
      <DataTypeSelect />
    </nav>
  );
};

export default Navbar;
