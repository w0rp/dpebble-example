ENTRY(main)

MEMORY
{
  APP (rwx) : ORIGIN = 0, LENGTH = 65536
}

SECTIONS
{
    .header :
    {
        KEEP(*(.pbl_header))

    } > APP

    /* This is sme junk for the PebbleProcessInfo struct */
    .note.gnu.build-id ALIGN(1) : {
        PROVIDE(BUILD_ID = .);
        KEEP(*(.note.gnu.build-id))
    } > APP

    .text :
    {
        *(.text)
        *(.text.*)
        *(.rodata)
        *(.rodata*)
    } > APP

    .data :
    {
        KEEP(*(.data))
        *(.data.*)
    } > APP

    .bss :
    {
        *(.bss)
        *(.bss.*)
    } > APP

    DISCARD :
    {
        libc.a ( * )
        libm.a ( * )
        libgcc.a ( * )
        *(.eh_frame)
    }
}
