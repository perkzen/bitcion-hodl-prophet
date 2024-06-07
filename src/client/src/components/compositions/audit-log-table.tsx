'use client';
import { CaretSortIcon, ChevronDownIcon } from '@radix-ui/react-icons';
import {
  ColumnDef,
  ColumnFiltersState,
  SortingState,
  VisibilityState,
  flexRender,
  getCoreRowModel,
  getFilteredRowModel,
  getPaginationRowModel,
  getSortedRowModel,
  useReactTable,
} from '@tanstack/react-table';

import {
  DropdownMenu,
  DropdownMenuCheckboxItem,
  DropdownMenuContent,
  DropdownMenuTrigger,
} from '@/components/ui/dropdown-menu';
import {
  Table,
  TableBody,
  TableCell,
  TableHead,
  TableHeader,
  TableRow,
} from '@/components/ui/table';
import { Button } from '../ui/button';
import { useState } from 'react';
import { AuditLog, DataType, ModelType } from '@/api';
import { useAuditLogs } from '@/api/hooks';
import DataTypeBadge from '@/components/compositions/data-type-badge';
import ModelTypeBadge from '@/components/compositions/model-type-badge';
import {
  Select,
  SelectContent,
  SelectGroup,
  SelectItem,
  SelectTrigger,
  SelectValue,
} from '@/components/ui/select';
import { formatDate } from '@/libs/utils';

export const columns: ColumnDef<AuditLog>[] = [
  {
    accessorKey: 'model_type',
    header: 'Model Type',
    cell: (cell) => {
      return <ModelTypeBadge type={cell.getValue() as ModelType} />;
    },
  },
  {
    accessorKey: 'data_type',
    header: 'Data Type',
    cell: (cell) => {
      return <DataTypeBadge type={cell.getValue() as DataType} />;
    },
  },
  {
    accessorKey: 'model_version',
    header: 'Model Version',
    cell: (cell) => {
      return `v${cell.getValue()}`;
    },
  },
  {
    accessorKey: 'prediction',
    header: 'Prediction',
    cell: (cell) => {
      return <code>{JSON.stringify(cell.getValue())}</code>;
    },
  },
  {
    accessorKey: 'created_at',
    header: ({ column }) => {
      return (
        <Button
          variant={'ghost'}
          onClick={() => column.toggleSorting(column.getIsSorted() === 'asc')}
        >
          Created At
          <CaretSortIcon className="ml-2 h-4 w-4" />
        </Button>
      );
    },
    cell: (cell) => {
      return formatDate(cell.getValue() as string);
    },
  },
];

export function AuditLogTable() {
  const [sorting, setSorting] = useState<SortingState>([]);
  const [columnFilters, setColumnFilters] = useState<ColumnFiltersState>([]);
  const [columnVisibility, setColumnVisibility] = useState<VisibilityState>({});
  const [rowSelection, setRowSelection] = useState({});

  const { data } = useAuditLogs();

  const table = useReactTable({
    data,
    columns,
    onSortingChange: setSorting,
    onColumnFiltersChange: setColumnFilters,
    getCoreRowModel: getCoreRowModel(),
    getPaginationRowModel: getPaginationRowModel(),
    getSortedRowModel: getSortedRowModel(),
    getFilteredRowModel: getFilteredRowModel(),
    onColumnVisibilityChange: setColumnVisibility,
    onRowSelectionChange: setRowSelection,
    state: {
      sorting,
      columnFilters,
      columnVisibility,
      rowSelection,
    },
  });

  const resetFilters = () => {
    setColumnFilters([]);
    table.setColumnFilters([]);
  };

  return (
    <div className="w-full">
      <div className="flex items-center py-4">
        <div className={'flex flex-row gap-4'}>
          <Select
            value={
              (table.getColumn('model_type')?.getFilterValue() as string) ?? ''
            }
            onValueChange={(s) =>
              table.getColumn('model_type')?.setFilterValue(s)
            }
          >
            <SelectTrigger className="w-[180px]">
              <SelectValue placeholder="Select a Model Type" />
            </SelectTrigger>
            <SelectContent className={'bg-neutral-800'}>
              <SelectGroup>
                <SelectItem value="reg">Regression</SelectItem>
                <SelectItem value="cls">Classification</SelectItem>
              </SelectGroup>
            </SelectContent>
          </Select>

          <Select
            value={
              (table.getColumn('data_type')?.getFilterValue() as string) ?? ''
            }
            onValueChange={(s) =>
              table.getColumn('data_type')?.setFilterValue(s)
            }
          >
            <SelectTrigger className="w-[180px]">
              <SelectValue placeholder="Select a Data Type" />
            </SelectTrigger>
            <SelectContent className={'bg-neutral-800'}>
              <SelectGroup>
                <SelectItem value="hourly">Hourly</SelectItem>
                <SelectItem value="daily">Daily</SelectItem>
              </SelectGroup>
            </SelectContent>
          </Select>

          <Button onClick={resetFilters} variant="outline">
            Reset
          </Button>
        </div>
        <DropdownMenu>
          <DropdownMenuTrigger asChild>
            <Button variant="outline" className="ml-auto">
              Columns <ChevronDownIcon className="ml-2 h-4 w-4" />
            </Button>
          </DropdownMenuTrigger>
          <DropdownMenuContent align="end">
            {table
              .getAllColumns()
              .filter((column) => column.getCanHide())
              .map((column) => {
                return (
                  <DropdownMenuCheckboxItem
                    key={column.id}
                    className="capitalize"
                    checked={column.getIsVisible()}
                    onCheckedChange={(value) => column.toggleVisibility(value)}
                  >
                    {column.id}
                  </DropdownMenuCheckboxItem>
                );
              })}
          </DropdownMenuContent>
        </DropdownMenu>
      </div>
      <div className="rounded-md border border-neutral-600">
        <Table>
          <TableHeader>
            {table.getHeaderGroups().map((headerGroup) => (
              <TableRow key={headerGroup.id}>
                {headerGroup.headers.map((header) => {
                  return (
                    <TableHead key={header.id}>
                      {header.isPlaceholder
                        ? null
                        : flexRender(
                            header.column.columnDef.header,
                            header.getContext()
                          )}
                    </TableHead>
                  );
                })}
              </TableRow>
            ))}
          </TableHeader>
          <TableBody>
            {table.getRowModel().rows?.length ? (
              table.getRowModel().rows.map((row) => (
                <TableRow
                  key={row.id}
                  data-state={row.getIsSelected() && 'selected'}
                >
                  {row.getVisibleCells().map((cell) => (
                    <TableCell key={cell.id}>
                      {flexRender(
                        cell.column.columnDef.cell,
                        cell.getContext()
                      )}
                    </TableCell>
                  ))}
                </TableRow>
              ))
            ) : (
              <TableRow>
                <TableCell
                  colSpan={columns.length}
                  className="h-24 text-center"
                >
                  No results.
                </TableCell>
              </TableRow>
            )}
          </TableBody>
        </Table>
      </div>
      <div className={'flex flex-row justify-between py-4'}>
        <span className="mx-2 font-light text-neutral-300 text-sm">
          Page {table.getState().pagination.pageIndex + 1} of{' '}
          {table.getPageCount()}
        </span>
        <div className={'flex gap-4'}>
          <Button
            variant="outline"
            onClick={() => table.previousPage()}
            disabled={!table.getCanPreviousPage()}
          >
            Previous
          </Button>

          <Button
            variant="outline"
            onClick={() => table.nextPage()}
            disabled={!table.getCanNextPage()}
          >
            Next
          </Button>
        </div>
      </div>
    </div>
  );
}
