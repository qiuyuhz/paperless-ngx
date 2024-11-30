import { Component } from '@angular/core'
import { NgbActiveModal } from '@ng-bootstrap/ng-bootstrap'
import {
  StorageType,
  SystemStatus,
  SystemStatusItemStatus,
} from 'src/app/data/system-status'
import { Clipboard } from '@angular/cdk/clipboard'
import { FileSizePipe } from 'src/app/pipes/file-size.pipe'

@Component({
  selector: 'pngx-system-status-dialog',
  templateUrl: './system-status-dialog.component.html',
  styleUrl: './system-status-dialog.component.scss',
  providers: [FileSizePipe],
})
export class SystemStatusDialogComponent {
  public SystemStatusItemStatus = SystemStatusItemStatus
  public StorageType = StorageType
  public status: SystemStatus

  public copied: boolean = false

  get paperlessStorageTotal(): number {
    return this.status
      ? this.status.storage.archive_total +
          this.status.storage.originals_total +
          this.status.storage.thumbnails_total +
          this.status.storage.data_total
      : 0
  }

  constructor(
    public activeModal: NgbActiveModal,
    private clipboard: Clipboard,
    private fileSizePipe: FileSizePipe
  ) {}

  public close() {
    this.activeModal.close()
  }

  public copy() {
    this.clipboard.copy(JSON.stringify(this.status, null, 4))
    this.copied = true
    setTimeout(() => {
      this.copied = false
    }, 3000)
  }

  public isStale(dateStr: string, hours: number = 24): boolean {
    const date = new Date(dateStr)
    const now = new Date()
    return now.getTime() - date.getTime() > hours * 60 * 60 * 1000
  }

  public getStatusPopover(status: StorageType): string {
    switch (status) {
      case StorageType.Originals:
        return [
          $localize`Originals`,
          this.fileSizePipe.transform(this.status.storage.originals_total),
        ].join(': ')
      case StorageType.Archive:
        return [
          $localize`Archive`,
          this.fileSizePipe.transform(this.status.storage.archive_total),
        ].join(': ')
      case StorageType.Thumbnails:
        return [
          $localize`Thumbnails`,
          this.fileSizePipe.transform(this.status.storage.thumbnails_total),
        ].join(': ')
      case StorageType.Data:
        return [
          $localize`Data`,
          this.fileSizePipe.transform(this.status.storage.data_total),
        ].join(': ')
    }
  }
}
